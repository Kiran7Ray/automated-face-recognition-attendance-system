from flask import Blueprint, request, jsonify
from services.student_service import *

student_bp = Blueprint("student", __name__)

@student_bp.route("/", methods=["POST"])
def add_student():
    data = request.json
    result = create_student(data)
    return jsonify(result)

@student_bp.route("/", methods=["GET"])
def get_students():
    return jsonify(get_all_students())

@student_bp.route("/<rollno>", methods=["DELETE"])
def delete_student_route(rollno):
    return jsonify(delete_student(rollno))