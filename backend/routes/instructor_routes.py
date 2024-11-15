from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime

instructor = Blueprint("instructor", __name__)

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