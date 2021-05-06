from celery import Celery
from kepy.settings import REDIS

app = Celery('tasks', broker=REDIS, backend=REDIS)

from kepy_worker.mute_worker import mute, unmute
