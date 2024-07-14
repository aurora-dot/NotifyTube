"""
    Command for collecting videos now
"""

from django.core.management.base import BaseCommand

from notifier.lib.database_iterator import collect_new_videos
from notifier.lib.logger import LOGGER


class Command(BaseCommand):
    """
    Command for collecting videos now
    """

    help = "Runs Collector."

    def handle(self, *args, **options):
        LOGGER.info("Collect Now: Start...")
        collect_new_videos()
        LOGGER.info("Collect Now: end...")
