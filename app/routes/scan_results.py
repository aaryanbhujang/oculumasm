from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from celery.result import AsyncResult
from app.celery_app import celery as celery_app  # This should be your Celery app instance
import logging
logging.basicConfig(level=logging.DEBUG)
import json
logger = logging.getLogger(__name__)
results_bp = Blueprint('results', __name__)

@results_bp.route('/scan_results/<task_id>', methods=['GET'])
def get_result_by_task(task_id):
    """
    Retrieve scan result from MongoDB using task_id
    """
    result = current_app.db.db.subdomains.find_one({'task_id': task_id})
    if not result:
        return jsonify({'error': 'Result not found'}), 404
    result['_id'] = str(result['_id'])  # Make ObjectId JSON serializable
    return jsonify(result), 200

@results_bp.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """
    Check task status and return detailed info.
    If task is successful, return both status and results.
    """
    result = AsyncResult(task_id, app=celery_app)
    status = result.status

    if status == 'PENDING':
        return jsonify({"status": "PENDING", "message": "Task not yet started"}), 202
    elif status == 'STARTED':
        return jsonify({"status": "STARTED", "message": "Task is in progress"}), 202
    elif status == 'FAILURE':
        return jsonify({"status": "FAILED", "error": str(result.info)}), 500
    elif status == 'SUCCESS':
        # Try to fetch associated scan result from DB
        record = current_app.db.db.subdomains.find_one({'task_id': task_id})
        logger.debug("[*]ACCESSING DB: %s", current_app.db.db.name)
        #logger.debug("[*]DB REQUEST: %s", json.dumps(record))
        if record:
            record['_id'] = str(record['_id'])
            return jsonify({"status": "COMPLETED", "data": record}), 200
        else:
            return jsonify({"status": "COMPLETED", "message": "Task done but result not found"}), 200

    return jsonify({"status": status, "message": "Unhandled task state"}), 200
