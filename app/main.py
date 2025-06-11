from flask import Flask
from app.routes.assets import assets_bp
from app.routes.scan_results import results_bp
from app.models.db import init_db  # or database if you renamed it
import os

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://mongo:27017/asm')    #app.config['SECRET_KEY'] = 'change_me'

    init_db(app)

    app.register_blueprint(assets_bp)
    app.register_blueprint(results_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
