# Import required frameworks/libraries
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os

# Import necessary files and functions from the project
from models import *
from routes.student_routes import student
from routes.instructor_routes import instructor
from routes.TA_routes import ta
from routes.admin_routes import admin
from routes.authentication import auth

# Initialize app
app = Flask(__name__)

# Setup CORS
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///collabspace_db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.app_context().push()
db.init_app(app)

# Initialize Flask migrate (allows to make changes to DB directly without deleting each time)
migrate = Migrate(app, db)

# Defines blueprints for routes based on users
app.register_blueprint(student)
app.register_blueprint(instructor)
app.register_blueprint(ta)
app.register_blueprint(admin)
app.register_blueprint(admin)

# JWT initializing for authentication
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
