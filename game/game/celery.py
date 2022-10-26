import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game.settings')

app = Celery('game')
app.config_from_object('django.conf:settings', namespace='CELERY')  # Celery will take all settings with 'CELERY' in
# at the beginning
app.autodiscover_tasks()  # automatically pull tasks

# # periodic tasks
# app.conf.beat_schedule = {
#     'send-spam-every-1-minutes': {
#         'task': 'main.tasks.send_beat_email',  # indicate task
#         'schedule': crontab(minute='*/1')  # every 3 minutes
#     },
# }
