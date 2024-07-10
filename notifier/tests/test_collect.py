"""Module providing tests for Collector class."""

import json
import re
from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from notifier.lib.collect import Collector


class CollectTestCase(StaticLiveServerTestCase):
    """Class for testing Collector class"""

    def _get_mock_page(self, page_path):
        browser = Collector()._setup_browser()  # pylint: disable=W0212
        browser.get(self.live_server_url + page_path)
        return browser

    @staticmethod
    def _remove_inconsistencies(data):
        for d in data:
            if d["thumbnail"] is not None:
                d["thumbnail"] = "/" + re.sub(
                    r"http:\/\/localhost:\d*?\/", "", d["thumbnail"]
                )

            if d["channel_img"] is not None:
                d["channel_img"] = "/" + re.sub(
                    r"http:\/\/localhost:\d*?\/", "", d["channel_img"]
                )

        return data

    @mock.patch("notifier.lib.collect.Collector._goto_query_page")
    def test_get_newest_videos_functions(self, mock_goto_query_page):

        # pos
        mock_goto_query_page.return_value = self._get_mock_page(
            "/static/tests/positive.html"
        )

        collector = Collector()
        positive = collector.get_latest_videos("hello world", "stYBPhSMp94")

        with open(
            "notifier/tests/collect/positive.json", "r", encoding="utf-8"
        ) as file:
            data = self._remove_inconsistencies(json.load(file))
            positive = self._remove_inconsistencies(positive)
            self.assertEqual(positive, data)

        # neg
        mock_goto_query_page.return_value = self._get_mock_page(
            "/static/tests/negative.html"
        )

        collector = Collector()
        self.assertRaises(
            LookupError, collector.get_latest_videos, "huybg", "doesntexist"
        )
        self.assertRaises(ValueError, collector.get_latest_videos, "", "")
        self.assertRaises(ValueError, collector.get_latest_videos, "h", "")
        self.assertRaises(ValueError, collector.get_latest_videos, "", "h")
