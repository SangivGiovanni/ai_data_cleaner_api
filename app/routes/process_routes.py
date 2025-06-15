from flask import Blueprint, jsonify, send_file
import os
import logging
from app.services.data_cleaning import map_and_clean_data
from app.config import UPLOAD_FOLDER

logger = logging.getLogger(__name__)

process_bp = Blueprint('process_routes', __name__)


@process_bp.route('/map_and_clean', methods=['GET'])
def map_and_clean():
    try:
        result = map_and_clean_data()
        logger.info(f"✅ Messy file has been mapped and cleaned")
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"❌ Error in map_and_clean: {e}")
        return jsonify({"error": "Processing failed", "details": str(e)}), 500


@process_bp.route('/download_cleaned', methods=['GET'])
def download_cleaned():
    path = os.path.join(UPLOAD_FOLDER, 'cleaned_output.xlsx')
    if os.path.exists(path):
        logger.info(f"📁 downloading file...")
        return send_file(path, as_attachment=True)
    logging.error(f"❌ Cleaned file does not exist?")
    return jsonify({"error": "Cleaned file not found"}), 404
