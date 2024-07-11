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


class Command(BaseCommand):
    """
    Scheduler for collecting newest videos for stored queries every hour
    """

    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        job_id = "collect_new_videos"

        LOGGER.info("Scheduler - %s: Adding job...", datetime.now())

        scheduler.add_job(
            collect_new_videos,
            trigger=CronTrigger(hour="*/1"),  # Every hour
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
