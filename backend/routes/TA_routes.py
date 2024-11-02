from flask import Blueprint, request, jsonify
from models import *

ta = Blueprint("ta", __name__)