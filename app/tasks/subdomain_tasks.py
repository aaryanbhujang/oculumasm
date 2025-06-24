# app/tasks/subdomain_tasks.py

import os, json, asyncio, redis
from typing import AsyncGenerator, Union
from celery.utils.log import get_task_logger

from app.celery_app import celery
from app.db import db as m
from app.modules.subdomain.run import run as scan_domains

logger = get_task_logger(__name__)

# Docker Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

@celery.task(bind=True, name="app.tasks.subdomain_tasks.scan")
def scan(self, domain: str):
    task_id        = self.request.id
    pubsub_channel = f"subd-stream:{task_id}"

    # kick off
    self.update_state(state='PROGRESS', meta={'stage': 'initializing', 'task_id': task_id})

    try:
        # run async generator
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        discovered: list[str] = []

        async def _process() -> None:
            async for item in scan_domains(domain):
                # stage markers
                if isinstance(item, dict) and 'stage' in item:
                    if item['stage'] == 'done':
                        return  # final result is in 'discovered'
                    r.publish(pubsub_channel, json.dumps(item))
                    self.update_state(state='PROGRESS', meta=item)
                # subdomain strings
                elif isinstance(item, str):
                    discovered.append(item)
                    msg = {"subdomain": item}
                    r.publish(pubsub_channel, json.dumps(msg))
                    self.update_state(state='PROGRESS', meta=msg)

        loop.run_until_complete(_process())

        # persist and grab the inserted_id
        record = {"task_id": task_id, "domain": domain, "subdomains": discovered}
        insert_result = m.db.subdomains.insert_one(record)
        oid = str(insert_result.inserted_id)
        logger.info(f"[✓] Inserted {len(discovered)} subdomains, _id={oid}")

        # final state
        self.update_state(state='COMPLETED', meta={'subdomains_found': len(discovered)})

        # return a JSON-safe payload
        return {
            "task_id":    task_id,
            "domain":     domain,
            "subdomains": discovered,
            "_id":        oid
        }

    except Exception as e:
        logger.exception(f"[!] Subdomain scan failed for {domain} | Task: {task_id}")
        self.update_state(state='FAILED', meta={'error': str(e)})
        raise
