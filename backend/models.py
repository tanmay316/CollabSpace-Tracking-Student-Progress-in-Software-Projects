from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String())
    email = db.Column(db.String(), nullable = False, unique = True)
    password_hash = db.Column(db.String(), nullable = False) 
    role = db.Column(db.String(), nullable = False)

# class Project(db.Model):

# class Milestones(db.Model):

# StudentTAChat(db.Model):

# class MentorshipSessions(db.Model):

# class AIChatbot(db.Model):

# class ChatbotInteractions(db.Model):

# class Feedback(db.Model):

# class StudentDoubts(db.Model):

# class VivaSlots(db.Model):

# class Alerts(db.Model):

    
'''
- could add github profile link to users table

  
'''