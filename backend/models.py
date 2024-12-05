from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String())
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    github_repo = db.Column(db.String(), nullable=True)  # only for students


class Milestones(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    date_issued = db.Column(db.Date(), nullable=False)
    deadline = db.Column(db.Date(), nullable=False)
    submissions = db.relationship("MilestoneSubmissions")


class MilestoneSubmissions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    milestone_id = db.Column(
        db.Integer(), db.ForeignKey("milestones.id"), nullable=False
    )
    student_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    github_branch_link = db.Column(db.String(), nullable=False)  # This is a GitHub link
    marks = db.Column(db.Integer(), nullable=True)
    instructor_feedback = db.Column(
        db.String(), nullable=True, default="No feedback required"
    )
    plagiarism_score = db.Column(db.Float(), nullable=True)  # Store plagiarism score
    plagiarism_status = db.Column(db.String(), nullable=True)


# Other models here...


# class InstructorFeedback(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     instructor_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
#     student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
#     milestone_id = db.Column(db.Integer(), db.ForeignKey('milestones.id'), nullable=False)
#     submission_id = db.Column(db.Integer(), db.ForeignKey('MilestoneSubmissions.id'), nullable=False)
#     feedback = db.Column(db.String(), nullable=False)


class MentorshipSessions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), default=200, nullable=True)
    mentor_name = db.Column(db.String(), nullable=False)
    registrations = db.relationship('MentorshipRegistrations')


class MentorshipRegistrations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    mentorship_session = db.Column(db.Integer(), db.ForeignKey('mentorship_sessions.id'), nullable=False)


class StudentDoubts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    doubt = db.Column(db.String(), nullable=False)
    responding_TA_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    response = db.Column(db.String(), nullable=False)


class ChatbotInteractions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(), nullable=False)
    response = db.Column(db.String(), nullable=False)


class VivaSlots(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Date(), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    examiner_name = db.Column(db.String(), nullable=False)
    status = db.Column(db.Boolean(), nullable=True)  # pass or fail status - will be updated after viva is over


# Requested by Raj
class ProjectData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(), nullable=False)
    enrollment_term = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
