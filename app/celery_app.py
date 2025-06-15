# app/celery_app.py

from celery import Celery

def make_celery():
    return Celery(
        'app',
        broker='redis://redis:6379/0',
        backend='redis://redis:6379/1',
        include=[
            'app.tasks.subdomain_tasks',
            # Add other task modules here
        ]
    )

celery = make_celery()
