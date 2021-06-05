import os
import dotenv
from celery import Celery
from kepy.settings.base import REDIS

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kepy.settings.development")
if settings := os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = settings

app = Celery('tasks', broker=REDIS, backend=REDIS)
app.config_from_object('django.conf:settings')

from kepy_worker.mute_tasks.tasks import mute, unmute
