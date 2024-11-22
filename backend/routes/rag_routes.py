from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import google.generativeai as genai
from utils.repo_utils import (
    is_valid_repolink,
    get_reponame,
    clone_github_repo,
    create_file_content_dict,
    delete_directory,
)
from utils.chat_utils import streamer, transform_stlit_to_genai_history
from utils.search_utils import make_all_files_content_str
import PyPDF2

rag = Blueprint("rag", __name__)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# State management
state = {
    "repo_details": {"name": "", "files2code": {}, "entire_code": ""},
    "uploaded_content": "",
    "messages": [],
    "title": "Provide a GitHub Repo link or Upload Files",
}


def process_uploaded_files(files):
    content = ""
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if filename.endswith(".pdf"):
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                pdf_text = "".join(page.extract_text() for page in reader.pages)
                content += f"===\nPDF: {filename}\n\n{pdf_text}\n\n"
        else:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content += f"===\nFile: {filename}\n\n{f.read()}\n\n"

    return content


@rag.route("/")
def home():
    return render_template("index.html", title=state["title"])


@rag.route("/submit", methods=["POST"])
def submit():
    repolink = request.form.get("repolink")
    files = request.files.getlist("files")

    if repolink:
        if not is_valid_repolink(repolink):
            return jsonify({"error": "Invalid GitHub repository link."}), 400
        try:
            clone_folder = get_reponame(repolink)
            reponame = clone_folder.replace("+", "/")
            repo_clone_path = f"./repo/{clone_folder}"
            clone_github_repo(repolink, repo_clone_path)
            repo_dict = create_file_content_dict(repo_clone_path)
            delete_directory(repo_clone_path)

            state["repo_details"]["name"] = reponame
            state["repo_details"]["files2code"] = repo_dict
            state["repo_details"]["entire_code"] = make_all_files_content_str(repo_dict)
            state["title"] = f"Chat with {reponame}"
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if files:
        state["uploaded_content"] = process_uploaded_files(files)
        state["title"] = "Chat with Uploaded Files"

    return jsonify({"message": "Setup complete. You can now chat!"})

@rag.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    state["messages"].append({"role": "user", "content": user_message})

    # Determine the relevant context
    if "github" in user_message.lower() and state["repo_details"]["entire_code"]:
        relevant_content = state["repo_details"]["entire_code"]
        source = "GitHub Repository"
    elif "file" in user_message.lower() and state["uploaded_content"]:
        relevant_content = state["uploaded_content"]
        source = "Uploaded Files"
    else:
        relevant_content = (
            state["uploaded_content"] or state["repo_details"]["entire_code"]
        )
        source = "Uploaded Files" if state["uploaded_content"] else "GitHub Repository"

    if not relevant_content:
        return jsonify(
            {
                "response": "No context available. Please upload files or provide a GitHub repository URL."
            }
        )

    input_to_LLM = f"Context Source: {source}\n\n'''\n{relevant_content}\n'''\nAnswer the following: {user_message}"
    genai_hist = transform_stlit_to_genai_history(
        state["messages"], -1, relevant_content
    )

    try:
        chat = model.start_chat(history=genai_hist)
        gemini_resp = chat.send_message(input_to_LLM, stream=True)
        assistant_response = "".join(streamer(gemini_resp))
    except Exception:
        assistant_response = "Sorry, an error occurred while processing your request."

    state["messages"].append({"role": "assistant", "content": assistant_response})
    return jsonify({"response": assistant_response})


@rag.route("/direct_chat", methods=["POST"])
def direct_chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    if "code" in user_message.lower():
        return jsonify(
            {"response": "Sorry, I cannot provide or generate code in this mode."}
        )

    try:
        chat = model.start_chat()
        gemini_resp = chat.send_message(user_message, stream=True)
        assistant_response = "".join(streamer(gemini_resp))
    except Exception:
        assistant_response = "Sorry, an error occurred while processing your request."

    return jsonify({"response": assistant_response})
