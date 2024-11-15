from flask import Blueprint, request, jsonify
from models import *

student = Blueprint("student", __name__)
