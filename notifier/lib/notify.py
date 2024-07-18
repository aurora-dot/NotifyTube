from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from notifier.models import Subscription, SubscriptionEmailFrequency, YouTubeVideo


def notify_hourly():
    notify_common(SubscriptionEmailFrequency.HOURLY)


def notify_daily():
    notify_common(SubscriptionEmailFrequency.DAILY)


def notify_weekly():
    notify_common(SubscriptionEmailFrequency.WEEKLY)


def notify_common(freq):
    for subscription in Subscription.objects.filter(email_frequency=freq):
        email = subscription.email.email
        query = subscription.query
        last_sent = subscription.last_sent
        new_videos = YouTubeVideo.objects.filter(
            youtube_query=query, created_at__gt=last_sent
        ).all()
        if len(new_videos) > 0:
            message = render_to_string(
                "emails/template.html",
                {
                    "email": email,
                    "query": query,
                    "new_videos": new_videos,
                    "subscription": subscription,
                },
            )
            send_mail(
                f"New YouTube Videos for: {query.query}",
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message,
            )
            # query.save()
