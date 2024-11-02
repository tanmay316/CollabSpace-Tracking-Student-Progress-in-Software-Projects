from flask import Blueprint, request, jsonify
from models import *

instructor = Blueprint("instructor", __name__)