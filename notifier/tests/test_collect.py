from datetime import UTC, datetime, timedelta

from django.test import TestCase

from notifier.lib.collect import Collector  # nopycln: import

# Create your tests here.


class CollectTestCase(TestCase):
    def setUp(self) -> None:
        self.collector = Collector()
        self.dt = datetime.now(UTC) - timedelta(days=1)

    def test_get_newest_videos_functions(self):

        youtube_list = self.collector._search(
            search_query="test",
            last_datetime=self.dt,
        )

        self.assertEqual(youtube_list["kind"], "youtube#searchListResponse")
        self.assertEqual(len(youtube_list["items"]), 50)

        self.assertIn("videoId", youtube_list["items"][0]["id"])
        self.assertIn("channelTitle", youtube_list["items"][0]["snippet"])

        stats_list = self.collector._get_video_statistics(youtube_list["items"])

        self.assertEqual(stats_list["kind"], "youtube#videoListResponse")
        self.assertEqual(len(stats_list["items"]), 50)

        self.assertIn("statistics", stats_list["items"][0])
        self.assertIn("viewCount", stats_list["items"][0]["statistics"])

        transformed_data = self.collector._transform_data(
            youtube_list["items"], stats_list["items"]
        )

        self.assertEqual(len(transformed_data), 50)
        self.assertEqual(
            "video_id,channel_title,channel_id,title,thumbnail,publish_time,views",
            ",".join(list(transformed_data[0].keys())),
        )

    def test_get_newest_videos_run(self):
        youtube_video_data = self.collector.run("test", self.dt)

        self.assertEqual(
            "video_id,channel_title,channel_id,title,thumbnail,publish_time,views",
            ",".join(list(youtube_video_data[0].keys())),
        )
        self.assertIn("test", youtube_video_data[0]["title"])
