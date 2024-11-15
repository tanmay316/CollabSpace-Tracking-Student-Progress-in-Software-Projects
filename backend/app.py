# Import required frameworks/libraries
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime

# Import necessary files and functions from the project
from models import *
from routes.student_routes import student
from routes.instructor_routes import instructor
from routes.TA_routes import ta
from routes.admin_routes import admin

# Initialize app
app = Flask(__name__)

# Setup CORS
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///LMS_v2_DB.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.app_context().push()
db.init_app(app)

# Initialize Flask migrate (allows to make changes to DB directly without deleting each time)
migrate = Migrate(app, db)

# Defines blueprints for routes based on users
app.register_blueprint(student, url_prefix="/api")
app.register_blueprint(instructor, url_prefix="/api")
app.register_blueprint(ta, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api")

# JWT intializing for authentication
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

# Project Status Endpoints
@app.route('/api/projects/status/<int:student_id>', methods=['GET'])
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

# Chat Endpoints
@app.route('/api/chat/instructor', methods=['POST'])
def send_message():
    data = request.json
    # need to complete
    return jsonify({'message': 'Message sent successfully'}), 201

@app.route('/api/chat/instructor', methods=['GET'])
def get_chat_history():
    student_id = request.args.get('student_id')
    instructor_id = request.args.get('instructor_id')
    # need to complete
    return jsonify({'messages': []})

# Doubts Endpoints
@app.route('/api/doubts', methods=['POST'])
def raise_doubt():
    data = request.json
    new_doubt = StudentDoubts(
        student_id=data['student_id'],
        doubt=data['doubt'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_doubt)
    db.session.commit()
    return jsonify({'message': 'Doubt raised successfully'}), 201

@app.route('/api/doubts', methods=['GET'])
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

# Milestone Comments Endpoints
@app.route('/api/milestones/comments', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)