from flask import Flask, jsonify

from models import *
from routes.student_routes import student
from routes.instructor_routes import instructor
from routes.TA_routes import ta
from routes.admin_routes import admin

app = Flask(__name__)

app.register_blueprint(student, url_prefix="/api")
app.register_blueprint(instructor, url_prefix="/api")
app.register_blueprint(ta, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)