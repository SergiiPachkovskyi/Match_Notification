from game.celery import app

from .models import Subscription
from .service import send
from .scraping import get_matches


@app.task
def new_subscription_notice(user_email, team_name):
    send(user_email, 'New team ' + team_name, 'New subscription')


@app.task()
def send_beat_email():
    for contact in Subscription.objects.all().select_related('user'):
        matches = get_matches(contact.team_name)
        if matches:
            send(contact.user.email, matches, f'{contact.team_name.title} future matches')
