from flask import Blueprint, request, jsonify
from models import *
from flask_jwt_extended import jwt_required, get_jwt

admin = Blueprint("admin", __name__)

@admin.route("/get_data", methods=["GET"])
@jwt_required() 
# @role_required("admin")
def get_data():
    try:
        records = alldata.query.with_entities(
            alldata.project_name,
            alldata.enrollment_term,
            alldata.completed
        ).all()

        data = [
            {
                "project_name": record.project_name,
                "enrollment_term": record.enrollment_term,
                "completed": record.completed
            }
            for record in records
        ]

        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500