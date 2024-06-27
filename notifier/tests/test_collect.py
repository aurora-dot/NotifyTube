from datetime import UTC, datetime, timedelta

from django.test import TestCase

from notifier.lib.collect import Collector  # nopycln: import

# Create your tests here.


class CollectTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_newest_videos(self):
        collector = Collector()
        dt = datetime.now(UTC) - timedelta(days=1)
        youtube_list = collector._search(
            search_query="test",
            last_datetime=dt,
        )

        self.assertEqual(youtube_list["kind"], "youtube#searchListResponse")
        self.assertEqual(len(youtube_list["items"]), 50)

        stats_list = collector._get_video_statistics(youtube_list["items"])
        transformed_data = collector._transform_data(
            youtube_list["items"], stats_list["items"]
        )

        print(transformed_data)
