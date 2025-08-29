# gunicorn.conf.py

import logging
from django.db import connections


logger = logging.getLogger("gunicorn.error")


workers = 4


def on_exit(server):
    logger.info("Gunicorn shutting down. Closing DB connections...")
    for conn in connections.all():
        try:
            conn.close()
        except Exception as e:
            logger.error(f"Error closing connection: {e}")


def worker_exit(server, worker):
    logger.info(f"Gunicorn worker {worker.pid} shutting down.")
    for conn in connections.all():
        try:
            conn.close()
        except Exception as e:
            logger.error(f"Error closing connection in worker: {e}")