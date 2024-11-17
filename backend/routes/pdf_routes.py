from flask import Blueprint, request, jsonify
from utils.pdf_utils import (
    get_pdf_text,
    get_text_chunks,
    get_vector_store,
    get_conversational_chain,
)
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

pdf = Blueprint("pdf", __name__)


@pdf.route("/upload", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")
    pdf_texts = [get_pdf_text([file]) for file in files]
    full_text = "".join(pdf_texts)
    text_chunks = get_text_chunks(full_text)
    get_vector_store(text_chunks)
    return jsonify({"message": "Files processed successfully."})


@pdf.route("/summarize", methods=["POST"])
def summarize_pdf():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    docs = vector_store.similarity_search("Summarize the document.")
    chain = get_conversational_chain()
    summary_response = chain(
        {"input_documents": docs, "question": "Summarize the document in detail"},
        return_only_outputs=True,
    )
    return jsonify({"summary": summary_response["output_text"]})


@pdf.route("/ask", methods=["POST"])
def ask_question():
    user_question = request.json.get("question")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    docs = vector_store.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )
    return jsonify({"response": response["output_text"]})
