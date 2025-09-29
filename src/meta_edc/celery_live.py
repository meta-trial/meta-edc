import os
import sys

from celery import Celery

# load settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.debug")

# config celery
app = Celery("meta_edc")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# app.conf.task_routes = {"*": {"queue": "live_queue"}}


@app.task(bind=True)
def debug_task(self):
    sys.stdout.write(f"Request: {self.request!r}\n")
