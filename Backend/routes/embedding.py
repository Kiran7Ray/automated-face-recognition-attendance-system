from flask import Blueprint, request, jsonify
from services.embedding_service import *

embedding_bp = Blueprint("embedding", __name__)

@embedding_bp.route("/", methods=["POST"])
def save_embedding():
    data = request.json
    return jsonify(store_embedding(data))

@embedding_bp.route("/match", methods=["POST"])
def match_embedding_route():
    data = request.json
    return jsonify(match_embedding(data["embedding"]))