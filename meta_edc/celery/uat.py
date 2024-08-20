import os

from celery import Celery

# load settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.uat")

# config celery
# remeber to include additional apps with tasks
app = Celery("meta_edc", include=["meta_reports"])
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
