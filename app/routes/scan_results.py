from flask import Blueprint, request, jsonify, current_app, Response
import redis
from datetime import datetime
from celery.result import AsyncResult
from app.celery_app import celery as celery_app  # This should be your Celery app instance
import logging
import os
logging.basicConfig(level=logging.DEBUG)
import json
logger = logging.getLogger(__name__)
results_bp = Blueprint('results', __name__)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

@results_bp.route('/stream/<scan_id>')
def stream_scan(scan_id):
    def event_generator():
        pubsub = redis_client.pubsub()
        pubsub.subscribe(f'subd-stream:{scan_id}')
        
        try:
            while True:
                message = pubsub.get_message(timeout=30)
                if message and message['type'] == 'message':
                    yield f"data: {message['data']}\n\n"
                else:
                    # Send keep-alive comment
                    yield ":keep-alive\n\n"
        finally:
            pubsub.close()
            print(f"Closed SSE connection for scan {scan_id}")

    return Response(event_generator(), mimetype='text/event-stream')

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
    Check task stat us and return detailed info.
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
