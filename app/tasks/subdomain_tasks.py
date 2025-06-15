from app.celery_app import celery
from app.modules.subdomain.run import run as scan_domains
from app.modules.subdomain.schemas import SubdomainResult
from app.db import db as m
from celery.utils.log import get_task_logger
import asyncio
import logging
logger = get_task_logger(__name__)
logging.basicConfig(level=logging.DEBUG)

@celery.task(bind=True, name="app.tasks.subdomain_tasks.scan")
def scan(self, domain: str):
    """Celery task to run subdomain enumeration"""
    self.update_state(state='PROGRESS', meta={'stage': 'passive'})
    
    try:
        result: SubdomainResult = asyncio.run(scan_domains(domain))
        logger.info("IMPORTED DB: %s", m.name)
        m.db.subdomains.insert_one({**result.dict(),"task_id": self.request.id})
        logger.info("[*]INSERTED IN: %s", m.name)
        logger.info("[*]INSERTION ID: %s", self.request.id)

        inserted_doc = m.db.subdomains.find_one({"task_id": self.request.id})
        if inserted_doc:
            logger.info("[*]INSERTED DOC BY TASK_ID: %s", inserted_doc)
        else:
            logger.info("[!] Document not found after insertion for task_id: %s", self.request.id)

        logger.info("TASK CREATED:%s", self.request.id)
        self.update_state(state='COMPLETED', meta={'subdomains_found': len(result.subdomains)})
        return result.dict()
    
    except Exception as e:
        logger.error(f"Subdomain scan failed: {e}")
        self.update_state(state='FAILED', meta={'error': str(e)})
        raise
