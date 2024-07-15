"""Module providing tests for Collector class."""

import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from notifier.lib.collect import Collector
from notifier.lib.metadata_extractor import MetadataExtractor


class CollectTestCase(StaticLiveServerTestCase):
    """Class for testing Collector class"""

    @staticmethod
    def _get_example_video_ids_for_test(query):
        collector = Collector()
        browser = collector._setup_browser()  # pylint: disable=W0212
        browser = collector._goto_query_page(query)  # pylint: disable=W0212

        extractor = MetadataExtractor()

        for _ in range(3):
            browser.execute_script(
                "window.scrollTo(0, 99999999999999999999999999999999)"
            )
            time.sleep(2)

        return [
            extractor.extract(video_element)["video"]["video_id"]
            for video_element in browser.find_elements(
                By.TAG_NAME, "ytd-video-renderer"
            )[-5:]
        ]

    def test_initial_add(self):
        """
        Tests collecting the newest video given a new query
        """
        collector = Collector()

        query_str = "test search"
        data = collector.get_initial_video_for_query(query_str)

        for _dict in data:
            self.assertEqual(len(_dict["video"]["video_id"]), 11)
            self.assertLessEqual(len(_dict["video"]["title"]), 100)
            self.assertIn("youtube.com", _dict["video"]["link"])
            self.assertIn("youtube.com", _dict["channel"]["channel_link"])

    def test_get_newest_videos_functions(self):
        """
        Test to check getting the newest videos with a given query and video id
        """

        query = "skibidi"
        last_five_videos = self._get_example_video_ids_for_test(query)

        # pos

        collector = Collector()
        positive = collector.get_latest_videos(query, last_five_videos)

        for _dict in positive:
            self.assertEqual(len(_dict["video"]["video_id"]), 11)
            self.assertLessEqual(len(_dict["video"]["title"]), 100)
            self.assertIn("youtube.com", _dict["video"]["link"])
            self.assertIn("youtube.com", _dict["channel"]["channel_link"])
            self.assertIn("ytimg.com", _dict["video"]["thumbnail"])
            self.assertIn("ggpht.com", _dict["channel"]["channel_img"])

        # none of the videos we got previously shouldn't be in the videos
        self.assertFalse(
            any([_dict["video"]["video_id"] in last_five_videos for _dict in positive])
        )

        # neg

        collector = Collector()
        self.assertRaises(
            LookupError, collector.get_latest_videos, query, ["doesntexist"], 5
        )
        self.assertRaises(ValueError, collector.get_latest_videos, "", "")
        self.assertRaises(ValueError, collector.get_latest_videos, "h", [])
        self.assertRaises(ValueError, collector.get_latest_videos, "h", None)
        self.assertRaises(ValueError, collector.get_latest_videos, "", "h")
