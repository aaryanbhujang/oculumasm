from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

results_bp = Blueprint('results', __name__)

@results_bp.route('/scan_results', methods=['POST'])
def receive_results():
    payload = request.get_json()
    # Expected: { domain, subdomains: [], ports: [] }
    record = {
        'domain': payload.get('domain'),
        'subdomains': payload.get('subdomains', []),
        'ports': payload.get('ports', []),
        'scanned_at': datetime.utcnow()
    }
    current_app.db.scan_results.insert_one(record)
    return jsonify({'status': 'success'}), 201