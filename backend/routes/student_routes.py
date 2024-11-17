from flask import Blueprint, request, jsonify
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # type: ignore

student = Blueprint("student", __name__)


@student.route('/api/projects/status/<int:student_id>', methods=['GET'])
def get_project_status(student_id):
    submissions = MilestoneSubmissions.query.filter_by(student_id=student_id).all()
    status_data = []

    for submission in submissions:
        milestone = Milestones.query.get(submission.milestone_id)
        status_data.append({
            'milestone_id': milestone.id,
            'title': milestone.title,
            'completion_status': 'completed' if submission.GitHub_repo_branch_link else 'pending',
            'deadline': milestone.deadline.isoformat()
        })

    return jsonify(milestone_progress=status_data)


@student.route("/link_github_repo", methods=["POST"])
@jwt_required()
# @role_required("student")
def link_github_repo():
    student_id = get_jwt_identity()
    data = request.get_json()
    github_repo_link = data.get("github_repo_link")

    if not github_repo_link:
        return jsonify({"error": "GitHub repository link is required"}), 400

    student = Users.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.Github = github_repo_link
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository linked successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/update_github_repo", methods=["PUT"])
@jwt_required()
# @role_required("student")
def update_github_repo():
    student_id = get_jwt_identity()
    data = request.get_json()
    new_github_repo_link = data.get("github_repo_link")

    if not new_github_repo_link:
        return jsonify({"error": "New GitHub repository link is required"}), 400

    student = Users.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.Github = new_github_repo_link
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/delete_github_repo", methods=["DELETE"])
@jwt_required()
# @role_required("student")
def delete_github_repo():
    student_id = get_jwt_identity()
    student = Users.query.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.Github = None
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/get_github_repo", methods=["GET"])
@jwt_required()
# @role_required("student")
def get_github_repo():
    student_id = get_jwt_identity()
    student = Users.query.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"github_repo_link": student.Github}), 200


@student.route("/home_page", methods=["GET"])
@jwt_required()
# @role_required("student")
def get_all_milestones():
    try:
        milestones = Milestones.query.all()
        milestones_data = [
            {
                "id": milestone.id,
                "title": milestone.title,
                "description": milestone.description,
                "issue_date": milestone.issue_date.strftime("%Y-%m-%d"),
                "deadline": milestone.deadline.strftime("%Y-%m-%d")
            }
            for milestone in milestones
        ]
        return jsonify({"milestones": milestones_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@student.route('/api/mentorship_sessions', methods=['GET'])
def list_mentorship_sessions():
    sessions = MentorshipSessions.query.all()
    result = [{"id": session.id, "description": session.description,
               "price": session.price, "mentor_name": session.mentor_name} for session in sessions]
    return jsonify(result)


@student.route('/api/mentorship_sessions/register', methods=['POST'])
def register_mentorship_session():
    data = request.get_json()
    try:
        registration = MentorshipRegistrations(
            student_id=data['student_id'],
            mentorship_session=data['session_id']
        )
        db.session.add(registration)
        db.session.commit()
        return jsonify({"message": "Registered for mentorship session successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
