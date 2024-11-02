from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from models import *
from routes.student_routes import student
from routes.instructor_routes import instructor
from routes.TA_routes import ta
from routes.admin_routes import admin

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///LMS_v2_DB.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.app_context().push()
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(student, url_prefix="/api")
app.register_blueprint(instructor, url_prefix="/api")
app.register_blueprint(ta, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api")

app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)