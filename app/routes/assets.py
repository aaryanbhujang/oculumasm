from flask import Blueprint, request, redirect, render_template, url_for, current_app, jsonify
import json
from datetime import datetime
from app.core import input_validation, workflow
from celery.exceptions import CeleryError
import logging
assets_bp = Blueprint('assets', __name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
@assets_bp.route('/', methods=['GET'])
def dashboard():
    assets = list(current_app.db.assets.find())
    return render_template('dashboard.html', assets=assets)

@assets_bp.route('/scan', methods=['POST'])
def create_scan():
    try:
        data = request.get_json()
        if not data or "target" not in data:
            return jsonify({"error": "Missing target"}), 400
        logger.info("RECEIVED: %s", json.dumps(data))
        normalized = input_validation.normalize_input(data["target"])
        logger.debug("VALIDATED: %s", json.dumps(normalized))
        available = workflow.get_available_modules(normalized["type"])
        logger.debug("AVAILABLE %s", json.dumps(available))
        selected = data.get("modules", available)
        logger.debug("SELECTED %s", json.dumps(selected))
        if not selected:
            return jsonify({"error": "No valid modules available"}), 400
        
        workflow_chain = workflow.create_workflow(normalized, selected)
        result = workflow_chain.apply_async()
        
        return jsonify({
            "scan_id": result.id,
            "modules": selected,
            "status_url": f"/results/{result.id}"
        }), 202
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except CeleryError:
        return jsonify({"error": "Task submission failed"}), 500