from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime
import requests
from urllib.parse import urlparse
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from Levenshtein import distance as levenshtein_distance

from routes.authentication import *
ta = Blueprint("ta", __name__)


@ta.route('/api/doubts', methods=['GET'])
def get_doubts():
    doubts = StudentDoubts.query.all()
    doubt_list = []
    for doubt in doubts:
        student = Users.query.get(doubt.student_id)
        doubt_list.append({
            'doubt_id': doubt.id,
            'student_name': f"{student.first_name} {student.last_name}",
            'doubt': doubt.doubt,
            'status': 'answered' if doubt.response else 'pending',
            'created_at': doubt.created_at.isoformat()
        })
    return jsonify(doubt_list)


@ta.route('/api/chat/ta', methods=['GET'])
def get_chat_history():
    data = request.get_json()
    student_id = data["student_id"]
    ta_id = data['ta_id']

    # student_id = request.args.get('student_id')
    # ta_id = request.args.get('ta_id')

    # chat_history = ChatbotInteractions.query.filter(
    #     (ChatbotInteractions.user_id == student_id) | (ChatbotInteractions.user_id == ta_id)
    # ).order_by(ChatbotInteractions.created_at).all()

    # messages = [
    #     {'query': interaction.query, 'response': interaction.response, 'timestamp': interaction.created_at.isoformat()}
    #     for interaction in chat_history
    # ]
    # if messages:
    #     return jsonify({'messages': messages})
        
    return jsonify({'message': "No chats found"})


@ta.route('/api/chat/ta', methods=['POST'])
def send_message():
    # data = request.json
    # new_message = ChatbotInteractions(
    #     user_id=data['ta_id'],
    #     query=data['message'],
    #     response=data['response'],
    #     created_at=datetime.utcnow()
    # )
    # db.session.add(new_message)
    # db.session.commit()
    return jsonify({'message': 'Message sent successfully'}), 201

# pending: student id?
# time: dynamic
@ta.route('/api/viva_slots', methods=['POST'])
def create_viva_slot():
    import datetime
    x = datetime.datetime.now()
    data = request.get_json()
    try:
        viva_slot = VivaSlots(
            time=x,
            # time=data['time'],
            # student_id=data['student_id'],
            student_id='None',
            examiner_name=data['examiner_name'],
            # examiner_name='None',
            status=False
        )
        db.session.add(viva_slot)
        db.session.commit()
        return jsonify({"message": "Viva slot created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ta.route('/api/viva_slots', methods=['GET'])
def fetch_viva_slots():
    slots = VivaSlots.query.all()
    result = [{"id": slot.id, "time": slot.time, "student_id": slot.student_id,
               "examiner_name": slot.examiner_name, "status": slot.status} for slot in slots]
    return jsonify(result)


@ta.route('/api/viva_slots/<int:slot_id>', methods=['POST'])
def update_viva_slot(slot_id):
    data = request.get_json()
    try:
        viva_slot = VivaSlots.query.get(slot_id)
        if viva_slot:
            viva_slot.time = data.get('time', viva_slot.time)
            viva_slot.status = data.get('status', viva_slot.status)
            viva_slot.examiner_name = data.get('examiner_name', viva_slot.examiner_name)
            db.session.commit()
            return jsonify({"message": "Viva slot updated successfully."})
        else:
            return jsonify({"error": "Viva slot not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ta.route('/api/viva_slots/<int:slot_id>', methods=['DELETE'])
def delete_viva_slot(slot_id):
    try:
        viva_slot = VivaSlots.query.get(slot_id)
        if viva_slot:
            db.session.delete(viva_slot)
            db.session.commit()
            return jsonify({"message": "Viva slot deleted successfully."})
        else:
            return jsonify({"error": "Viva slot not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

##############plag##################################################################################


def fetch_github_code(repo_url):
    try:
        # Extract the username and repo name from the GitHub URL
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            return None  # Invalid URL format
        user, repo = path_parts[:2]

        # GitHub API to fetch the content of the repository files
        api_url = f"https://api.github.com/repos/{user}/{repo}/contents"
        headers = {
            "Accept": "application/vnd.github.v3.raw"
            # 'Authorization': 'token YOUR_PERSONAL_ACCESS_TOKEN'  # Optional: Use if rate limits are an issue
        }
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            contents = response.json()
            files_content = []
            for file in contents:
                if file["type"] == "file" and file["name"].endswith(
                    (".py", ".java", ".c", ".cpp", ".js", ".ts", ".html", ".css")
                ):
                    file_response = requests.get(file["download_url"])
                    if file_response.status_code == 200:
                        files_content.append(file_response.text)
            return "\n".join(
                files_content
            )  # Return the combined code as a single string
        else:
            print(f"Failed to fetch repo contents: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching GitHub code: {e}")
        return None


# Function to compare two pieces of code
def compare_code(code1, code2):
    """
    Compare two pieces of code for similarity using Levenshtein distance and Cosine similarity.
    Returns a similarity score between 0 and 100.
    """
    if not code1 or not code2:
        return 0  # If either of the code snippets is empty, return 0% similarity

    # Compute similarity using both Levenshtein and Cosine Similarity
    lev_score = levenshtein_similarity(code1, code2)
    cosine_score = cosine_similarity(code1, code2)

    # Combine the scores (weighted equally)
    final_score = (lev_score * 0.5) + (cosine_score * 0.5)

    return final_score


# Levenshtein Distance-based Similarity
def levenshtein_similarity(str1, str2):
    # Normalize by string length for a percentage similarity
    lev_distance = levenshtein_distance(str1, str2)
    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 100  # Both strings are empty
    return (1 - lev_distance / max_len) * 100


# Cosine Similarity-based approach
def cosine_similarity(str1, str2):
    # Use CountVectorizer to convert text to a matrix of token counts
    vectorizer = CountVectorizer().fit_transform([str1, str2])
    vectors = vectorizer.toarray()
    numerator = np.dot(vectors[0], vectors[1])
    denominator = np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1])
    if denominator == 0:
        return 0
    cosine_score = numerator / denominator
    return cosine_score * 100  # Return as percentage


@ta.route("/api/check_plagiarism", methods=["POST"])
def check_plagiarism():
    data = request.get_json()

    if not data or "github_repo_link" not in data or "student_name" not in data:
        return (
            jsonify({"error": "GitHub repository link and student name are required"}),
            400,
        )

    new_repo_url = data["github_repo_link"]
    student_name = data["student_name"]

    new_repo_code = fetch_github_code(new_repo_url)

    if new_repo_code is None:
        return (
            jsonify(
                {
                    "error": "Unable to fetch repository data from GitHub. Please check the repository link."
                }
            ),
            500,
        )

    # Fetch all other student repository links from the database
    other_submissions = MilestoneSubmissions.query.join(
        Users, MilestoneSubmissions.student_id == Users.id
    ).all()
    plagiarism_results = []
    total_score = 0
    comparison_count = 0

    for submission in other_submissions:
        if submission.github_branch_link == new_repo_url:
            continue  # Skip comparing the same repository

        existing_repo_code = fetch_github_code(submission.github_branch_link)

        if existing_repo_code is None:
            continue  # Skip if no valid code is found for the repository

        # Compare the new submission with the existing submission
        score = compare_code(new_repo_code, existing_repo_code)
        total_score += score
        comparison_count += 1

        # Store the result with a pass/fail status (e.g., fail if score >= 30%)
        status = (
            "fail" if score >= 30 else "pass"
        )  # Set threshold (e.g., 30% similarity threshold)

        # Fetch the student name from the Users table
        student = Users.query.get(submission.student_id)
        student_full_name = (
            f"{student.first_name} {student.last_name}" if student else "Unknown"
        )

        plagiarism_results.append(
            {
                "student_name": student_full_name,
                "repo_link": submission.github_branch_link,
                "score": score,
                "status": status,
            }
        )

    overall_score = (total_score / comparison_count) if comparison_count > 0 else 0

    return (
        jsonify(
            {"overall_score": overall_score, "plagiarism_results": plagiarism_results}
        ),
        200,
    )
