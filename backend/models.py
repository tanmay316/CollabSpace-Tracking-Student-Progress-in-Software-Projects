from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String())
    email = db.Column(db.String(), nullable = False, unique = True)
    password_hash = db.Column(db.String(), nullable = False) 
    role = db.Column(db.String(), nullable = False)
    
'''
- could add github profile link to users table

project (GitHub link as one of the attributes), mentorship sessions, milestones, student doubts(for TA), feedback on project, viva slots, AI (need to figure out exact config),   
'''