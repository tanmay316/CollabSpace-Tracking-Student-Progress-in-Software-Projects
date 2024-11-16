from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt # type: ignore

instructor = Blueprint("instructor", __name__)

def validate_milestone_input(data):
    errors = []
    if not data.get("title"):
        errors.append("Title is required.")
    if not data.get("description"):
        errors.append("Description is required.")
    if not data.get("issue_date"):
        errors.append("Issue date is required.")
    if not data.get("deadline"):
        errors.append("Deadline is required.")
    return errors

@instructor.route('/api/milestones/comments', methods=['POST'])
def add_milestone_comment():
    data = request.json
    new_feedback = InstructorFeedback(
        milestone_id=data['milestone_id'],
        student_id=data['student_id'],
        feedback=data['comment'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201

@instructor.route("/create_milestone", methods=["POST"])
@jwt_required() 
# @role_required("instructor")
def create_milestone():
    data = request.get_json()
    errors = validate_milestone_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_milestone = Milestones(
            title=data["title"],
            description=data["description"],
            issue_date=datetime.strptime(data["issue_date"], "%Y-%m-%d"),
            deadline=datetime.strptime(data["deadline"], "%Y-%m-%d")
        )
        db.session.add(new_milestone)
        db.session.commit()
        return jsonify({"message": "Milestone created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@instructor.route("/milestones", methods=["GET"])
# @role_required("instructor") 
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

@instructor.route("/update_milestone/<int:milestone_id>", methods=["PUT"])
@jwt_required() 
# @role_required("instructor") 
def update_milestone(milestone_id):
    milestone = Milestones.query.get(milestone_id)
    if milestone is None:
        return jsonify({"error": "Milestone not found"}), 404

    data = request.get_json()
    milestone.title = data.get("title", milestone.title)
    milestone.description = data.get("description", milestone.description)
    if "issue_date" in data:
        milestone.issue_date = datetime.strptime(data["issue_date"], "%Y-%m-%d")
    if "deadline" in data:
        milestone.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")

    try:
        db.session.commit()
        return jsonify({"message": "Milestone updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@instructor.route("/delete_milestone/<int:milestone_id>", methods=["DELETE"])
@jwt_required() 
# @role_required("instructor")
def delete_milestone(milestone_id):
    milestone = Milestones.query.get(milestone_id)
    if milestone is None:
        return jsonify({"error": "Milestone not found"}), 404

    try:
        db.session.delete(milestone)
        db.session.commit()
        return jsonify({"message": "Milestone deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
