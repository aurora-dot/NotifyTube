from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from notifier.lib.collect import Collector
from notifier.lib.database_iterator import add_new_search_query, collect_new_videos
from notifier.models import YouTubeChannel, YouTubeQuery, YouTubeVideo


class DatabaseFunctionsTestCase(StaticLiveServerTestCase):
    """
    Tests for the database_iterator functions
    """

    def _mock_goto_query_page(self):
        browser = Collector()._setup_browser()  # pylint: disable=W0212
        browser.get(self.live_server_url + "/static/tests/positive.html")
        return browser

    # failing
    def test_initial_add(self):
        """
        Tests collecting the newest video given a new query
        """

        query_str = "test search"
        add_new_search_query(query_str)

        query_obj = YouTubeQuery.objects.get(query=query_str)
        self.assertEqual(query_obj.query, query_str)
        self.assertEqual(len(query_obj.latest.video_id), 11)
        self.assertLessEqual(len(query_obj.latest.title), 100)
        self.assertIn("youtube.com", query_obj.latest.link)
        self.assertIn("youtube.com", query_obj.latest.youtube_channel.channel_link)

    @mock.patch("notifier.lib.collect.Collector._goto_query_page")
    def test_collect_new_videos(self, mock_goto_query_page):
        """
        Tests collecting newest videos from a saved query
        """
        mock_goto_query_page.return_value = self._mock_goto_query_page()

        query_str = "hello world"
        query = YouTubeQuery(query=query_str)
        channel = YouTubeChannel(
            channel_link="https://www.youtube.com",
            channel_name="example",
            channel_img="https://example.com",
        )
        video = YouTubeVideo(
            video_id="wyALgqlfLsk",  # an id within the test page
            link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            title="Totally not a Rick Roll",
            thumbnail="https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg",
            youtube_query=query,
            youtube_channel=channel,
        )

        query.save()
        channel.save()
        video.save()

        query.latest = video
        query.save()

        collect_new_videos()

        for video in YouTubeVideo.objects.filter(youtube_query=query):
            self.assertEqual(video.youtube_query.query, query_str)
            self.assertEqual(len(video.video_id), 11)
            self.assertLessEqual(len(video.title), 100)
            self.assertTrue("youtube.com" in video.link)
            self.assertTrue("youtube.com" in video.youtube_channel.channel_link)
