from flask import Blueprint, request, jsonify
from models import *

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
  
