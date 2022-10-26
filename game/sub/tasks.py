from game.celery import app

from .models import Subscription
from .service import send


@app.task
def new_subscription_notice(user_email, team_name):
    send(user_email, 'New team ' + team_name, 'New subscription')


# @app.task
# def send_beat_email():
#     for contact in Subscription.objects.all():
#         send(contact.user.email, 'we will send yuo lot of messages every 1 minutes', 'Нова підписка')
#
#
# @app.task
# def my_task(a, b):
#     return a + b
#
#
# @app.task(bind=True, default_retry_delay=5*60)
# def my_task_retry(self, a, b):
#     try:
#         return a + b
#     except Exception as exc:
#         raise self.retry(exc=exc, countdown=60)
