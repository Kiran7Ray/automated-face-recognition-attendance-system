from flask import Blueprint, request, jsonify
from services.attendance_service import *

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/", methods=["POST"])
def mark_attendance():
    data = request.json
    return jsonify(create_attendance(data))

@attendance_bp.route("/", methods=["GET"])
def get_attendance():
    return jsonify(get_all_attendance())