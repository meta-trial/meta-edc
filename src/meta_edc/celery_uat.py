import os
import sys

from celery import Celery

# from kombu import Queue

# load settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.debug")

# config celery
app = Celery("meta_edc")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# app.conf.task_default_queue = "workuatq1"
# app.conf.task_queues = (Queue("workuatq1", routing_key="task.#"),)
# app.conf.task_default_exchange = "workuatq1"
# app.conf.task_default_exchange_type = "topic"
# app.conf.task_default_routing_key = "task.workuatq1"


@app.task(bind=True)
def debug_task(self):
    sys.stdout.write(f"Request: {self.request!r}\n")
