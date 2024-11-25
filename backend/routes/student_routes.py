from flask import Blueprint, request, jsonify
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # type: ignore

from routes.authentication import *

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
# @jwt_required()
# @role_required("student")
def link_github_repo():
    # student_id = get_jwt_identity()
    data = request.get_json()
    student_id = data["student_id"]
    github_repo_link = data.get("github_repo_link")

    if not github_repo_link:
        return jsonify({"error": "GitHub repository link is required"}), 400

    student = Users.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.github_repo = github_repo_link
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository linked successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/update_github_repo", methods=["PUT"])
# @jwt_required()
# @role_required("student")
def update_github_repo():
    # student_id = get_jwt_identity()
    data = request.get_json()
    student_id = data["student_id"]

    new_github_repo_link = data.get("github_repo_link")

    if not new_github_repo_link:
        return jsonify({"error": "New GitHub repository link is required"}), 400

    student = Users.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.github_repo = new_github_repo_link
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/delete_github_repo", methods=["POST"])
# @jwt_required()
# @role_required("student")
def delete_github_repo():
    # student_id = get_jwt_identity()

    data = request.get_json()
    student_id = data["student_id"]
    student = Users.query.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.github_repo = ""
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/get_github_repo", methods=["GET"])
# @jwt_required()
# @role_required("student")
def get_github_repo():
    # student_id = get_jwt_identity()
    data = request.get_json()
    student_id = data["student_id"]
    student = Users.query.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"github_repo_link": student.github_repo}), 200


# completion status -> if any submission made before deadline
@student.route("/milestones", methods=["GET"])
# @jwt_required()
# @role_required("student")
def get_all_milestones():
    try:
        milestones = Milestones.query.all()
        milestones_data = [
            {
                "id": milestone.id,
                "title": milestone.title,
                "description": milestone.description,
                "date_issued": milestone.date_issued.strftime("%Y-%m-%d"),
                "deadline": milestone.deadline.strftime("%Y-%m-%d")
            }
            for milestone in milestones
        ]
        return jsonify({"milestones": milestones_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# create mentorship session()
# delete mentorship session()
# update mentorship session()
@student.route('/mentorship_sessions', methods=['GET'])
def list_mentorship_sessions():
    sessions = MentorshipSessions.query.all()
    result = [{"id": session.id, "description": session.description,
               "price": session.price, "mentor_name": session.mentor_name} for session in sessions]
    return jsonify(result)


#pending
#  book_viva_slots()
@student.route('/book_viva_slot', methods=['POST'])
def book_viva_slot():
    vivaSlot = VivaSlots.query.get(id)
    if not vivaSlot:
        return jsonify({
            "message": "viva slot doesn't exist"
        }), 404

    if vivaSlot:
        vivaSlot.status = true

    db.session.commit()
    return jsonify({"message": "Viva slot booked successfully."}), 201


# make_milestone_submissions() -> rag, submit()

# pending
@student.route('/mentorship_sessions/register', methods=['POST'])
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


@student.route("/submit_milestone/<int:milestone_id>", methods=["POST"])
# @role_required("student")
def submit_milestone(milestone_id):
    """
    Allowed only once
    """
    if not Milestones.query.get(milestone_id):
        return jsonify({
            "message": "This milestone doesn't exist"
        }), 400

    data = request.get_json()
    branch_link = data.get("github_branch_link")

    new_submission = MilestoneSubmissions(
        milestone_id=milestone_id,
        # student_id=get_jwt_identity(),
        student_id=data['student_id'],
        github_branch_link=branch_link
    )

    db.session.add(new_submission)
    db.session.commit()

    return jsonify({
        "message": "Submitted Successfully"
    }), 200


@student.route("/get_submission/<int:milestone_id>", methods=["GET"])
@role_required("student")
def get_submission(milestone_id):
    """
    If no submission has been made yet, the submission form should be available. If a submission has been made,
    the GitHub link, feedback and marks should be displayed. Editing milestones is not allowed
    """

    submission = MilestoneSubmissions.query.filter_by(student_id=get_jwt_identity(), milestone_id=milestone_id).first()
    if not submission:
        return jsonify({
            "message": "No submission made yet"
        }), 400

    submission_details = {
        "id": submission.id,
        "student_id": submission.student_id,
        "milestone_id": submission.milestone_id,
        "github_branch_link": submission.github_branch_link,
        "instructor_feedback": submission.instructor_feedback,
        "marks": submission.marks
    }

    return jsonify({
        "submission_details": submission_details
    }), 200
