# Import required frameworks/libraries
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os
from flask_mail import Mail, Message
from celery.schedules import crontab
from celery import Celery

# Import necessary files and functions from the project
from models import *
from routes.student_routes import student
from routes.instructor_routes import instructor
from routes.TA_routes import ta
from routes.admin_routes import admin
from routes.authentication import auth
from routes.rag_routes import rag 
from routes.pdf_routes import pdf

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
app.register_blueprint(student, url_prefix="/api/student")
app.register_blueprint(instructor, url_prefix="/api/instructor")
app.register_blueprint(ta, url_prefix="/api/ta")
app.register_blueprint(admin, url_prefix="/api/admin")
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(rag, url_prefix="/api/rag")
app.register_blueprint(pdf, url_prefix="/api/pdf")

# JWT initializing for authentication
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025           
app.config['MAIL_USERNAME'] = None      
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

if __name__ == '__main__':
    app.run(debug=True)
