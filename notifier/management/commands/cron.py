"""
Scheduler for collecting newest videos for stored queries every hour
"""

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from notifier.lib.database_iterator import collect_new_videos
from notifier.lib.logger import LOGGER
from notifier.lib.notify import notify_daily, notify_hourly, notify_weekly


class Command(BaseCommand):
    """
    Scheduler for collecting newest videos for stored queries every hour
    """

    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        crons = {
            "collect_new_videos": (
                collect_new_videos,
                CronTrigger(hour="0-23", minute="30"),
            ),
            "hourly_email_notification": (notify_hourly, CronTrigger(hour="*/1")),
            "daily_email_notification": (notify_daily, CronTrigger(day="*/1")),
            "weekly_email_notification": (notify_weekly, CronTrigger(week="*/1")),
        }

        for job_id, tup in crons.items():
            function, trigger = tup

            LOGGER.info("Scheduler - %s: Adding job...", datetime.now())

            scheduler.add_job(
                func=function,
                trigger=trigger,
                id=job_id,
                max_instances=1,
                replace_existing=True,
            )

            LOGGER.info("Scheduler - %s: Added job '%s'.", datetime.now(), job_id)

        try:
            LOGGER.info("Scheduler - %s: Starting scheduler...", datetime.now())
            scheduler.start()
        except KeyboardInterrupt:
            LOGGER.info("Scheduler - %s: Stopping scheduler...", datetime.now())
            scheduler.shutdown()
            LOGGER.info(
                "Scheduler - %s: Scheduler shut down successfully!", datetime.now()
            )
