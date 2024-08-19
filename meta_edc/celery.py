import os
import sys
from pathlib import Path

import environ
from celery import Celery

env = environ.Env()

# find ENV file
if "test" in sys.argv:
    env_file = Path(__file__).parent.parent / ".env-tests"
    env.read_env(env_file)
    print(f"Reading env from {env_file}")
else:
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        raise FileExistsError(f"Environment file does not exist. Got `{env_file}`")
    env.read_env(env_file)

# load settings
if env("DJANGO_DEBUG"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.debug")
elif not env("DJANGO_LIVE_SYSTEM"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.uat")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.live")

# config celery
# remeber to include additional apps with tasks
app = Celery("meta_edc", include=["meta_reports"])
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
