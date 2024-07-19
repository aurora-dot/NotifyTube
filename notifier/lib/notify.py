from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from notifier.lib.logger import LOGGER
from notifier.models import Subscription, SubscriptionEmailFrequency, YouTubeVideo


def notify_hourly():
    LOGGER.info("Notifier - %s: Started hourly", datetime.now())
    notify_common(SubscriptionEmailFrequency.HOURLY)


def notify_daily():
    LOGGER.info("Notifier - %s: Started hourly", datetime.now())
    notify_common(SubscriptionEmailFrequency.DAILY)


def notify_weekly():
    LOGGER.info("Notifier - %s: Started hourly", datetime.now())
    notify_common(SubscriptionEmailFrequency.WEEKLY)


def notify_common(freq):
    for subscription in Subscription.objects.filter(email_frequency=freq):
        LOGGER.info(
            "Notifier - %s: Emailing subscribers for query %s",
            datetime.now(),
            subscription.query.query,
        )
        email = subscription.email.email
        query = subscription.query
        last_sent = subscription.last_sent
        new_videos = (
            YouTubeVideo.objects.filter(youtube_query=query, created_at__gt=last_sent)
            .order_by("-created_at")
            .all()
        )
        if len(new_videos) > 0:
            message = render_to_string(
                "emails/template.html",
                {
                    "email": email,
                    "query": query,
                    "new_videos": new_videos,
                    "subscription": subscription,
                    "domain": settings.DOMAIN,
                },
            )
            send_mail(
                f"New YouTube Videos for: {query.query}",
                f"{len(new_videos)} new videos found.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message,
            )
            subscription.save()
            LOGGER.info(
                "Notifier - %s: Sent emails for query %s",
                datetime.now(),
                subscription.query.query,
            )
