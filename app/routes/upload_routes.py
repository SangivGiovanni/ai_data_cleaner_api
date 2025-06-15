from flask import Blueprint, request, jsonify
import os
import logging
from app.config import UPLOAD_FOLDER

logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload_routes', __name__)


@upload_bp.route('/upload_template', methods=['POST'])
def upload_template():
    if 'file' not in request.files:
        logger.warning("⚠️ Upload attempt without a file part.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.warning("⚠️ Upload attempt with empty filename.")
        return jsonify({"error": "No selected file"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, 'template.xlsx')
    file.save(save_path)
    logger.info(f"✅ Template file saved to {save_path}")
    return jsonify({"message": "Template uploaded successfully", "saved_as": save_path}), 200


@upload_bp.route('/upload_messy', methods=['POST'])
def upload_messy():
    if 'file' not in request.files:
        logger.warning("⚠️ Upload attempt without a file part.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.warning("⚠️ Upload attempt with empty filename.")
        return jsonify({"error": "No selected file"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, 'messy.xlsx')
    file.save(save_path)
    logger.info(f"✅ Messy file saved to {save_path}")
    return jsonify({"message": "Messy file uploaded successfully", "saved_as": save_path}), 200
