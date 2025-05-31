from flask import Flask
from routes.assets import assets_bp
from routes.scan_results import results_bp
from models.db import init_db  # or database if you renamed it

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = "mongodb+srv://aaryan:aaryanistheadmin@pyasm.oysetm2.mongodb.net/pyasm_db?retryWrites=true&w=majority&appName=pyasm"  # Make sure this is set
    #app.config['SECRET_KEY'] = 'change_me'

    init_db(app)

    app.register_blueprint(assets_bp)
    app.register_blueprint(results_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
