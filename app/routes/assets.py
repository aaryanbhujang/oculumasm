from flask import Blueprint, request, redirect, render_template, url_for, current_app
from datetime import datetime

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/', methods=['GET'])
def dashboard():
    assets = list(current_app.db.assets.find())
    return render_template('dashboard.html', assets=assets)

@assets_bp.route('/submit', methods=['POST'])
def submit_asset():
    domain = request.form.get("domain")
    if not domain:
        return redirect(url_for("main.dashboard"))

    subdomains = runSubfinder(domain)
    timestamp = datetime.utcnow()

    for sub in subdomains:
        mongo.db.assets.insert_one({
            "domain": sub,
            "parent_domain": domain,
            "submitted_at": timestamp,
            "status": "pending",
            "vulnerabilities": []
        })

    return redirect(url_for("main.dashboard"))