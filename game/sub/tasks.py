from game.celery import app

from .models import Subscription, Match
from .service import send
from .scraping import get_matches


@app.task
def new_subscription_notice(user_email, team_name):
    send(user_email, 'New team ' + team_name, 'New subscription')


@app.task()
def send_beat_email():
    for contact in Subscription.objects.all().select_related('user'):
        matches = get_matches(contact.team_name)

        for match in matches:
            count = Match.objects.filter(user=contact.user,
                                         team_name=contact.team_name,
                                         event_date=match.event_date
                                         ).count()
            if count != 0:
                continue

            send(contact.user.email, match.link, f'{match.title} - {match.date}')

            new_match = Match(**match, user=contact.user)
            new_match.save()
