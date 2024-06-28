"""Module providing tests for Collector class."""

from datetime import UTC, datetime, timedelta

from django.test import TestCase

from notifier.lib.collect import Collector


class CollectTestCase(TestCase):
    """Class for testing Collector class"""

    def setUp(self) -> None:
        self.collector = Collector()
        self.dt = datetime.now(UTC) - timedelta(hours=1)

    def test_get_newest_videos_functions(self):
        """Testing each individual function of Collector to see if each stage works."""

        youtube_list = self.collector._search(  # pylint: disable=W0212
            search_query="test",
            last_datetime=self.dt,
        )

        self.assertGreaterEqual(len(youtube_list), 50)
        self.assertIn("videoId", youtube_list[0]["id"])
        self.assertIn("channelTitle", youtube_list[0]["snippet"])

        stats_list = self.collector._get_video_statistics(  # pylint: disable=W0212
            youtube_list
        )

        self.assertEqual(stats_list["kind"], "youtube#videoListResponse")
        self.assertEqual(len(stats_list["items"]), 50)

        self.assertIn("statistics", stats_list["items"][0])
        self.assertIn("viewCount", stats_list["items"][0]["statistics"])

        transformed_data = self.collector._transform_data(  # pylint: disable=W0212
            youtube_list["items"], stats_list["items"]
        )

        self.assertEqual(len(transformed_data), 50)
        self.assertEqual(
            "video_id,channel_title,channel_id,title,thumbnail,publish_time,views",
            ",".join(list(transformed_data[0].keys())),
        )

    def test_get_newest_videos_run(self):
        """Test if the full run function works for Collector."""

        youtube_video_data = self.collector.run("test", self.dt)

        self.assertEqual(
            "video_id,channel_title,channel_id,title,thumbnail,publish_time,views",
            ",".join(list(youtube_video_data[0].keys())),
        )
        self.assertIn("test", youtube_video_data[0]["title"])
