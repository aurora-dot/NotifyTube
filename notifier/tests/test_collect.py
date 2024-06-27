from datetime import datetime

from django.test import TestCase

from notifier.lib.collect import Collector  # nopycln: import

# Create your tests here.


class CollectTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_newest_videos(self):
        collector = Collector()
        out = collector.search(search_query="test", last_datetime=datetime.now())
        print(out)
