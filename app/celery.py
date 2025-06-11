from celery import Celery
from flask import Flask

def make_flask_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/1'
    )
    return app

def create_celery(app: Flask):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery

# This is what Celery expects when using `-A app.celery`
flask_app = make_flask_app()
celery = create_celery(flask_app)
