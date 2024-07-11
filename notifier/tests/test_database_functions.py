from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from notifier.lib.collect import Collector
from notifier.lib.database_iterator import add_new_search_query, collect_new_videos
from notifier.models import YouTubeChannel, YouTubeQuery, YouTubeVideo


class DatabaseFunctionsTestCase(StaticLiveServerTestCase):
    @mock.patch("notifier.lib.collect.Collector._goto_query_page")
    def test_initial_add(self, mock_goto_query_page):
        browser = Collector()._setup_browser()  # pylint: disable=W0212
        browser.get(self.live_server_url + "/static/tests/positive.html")
        mock_goto_query_page.return_value = browser

        query_str = "test search"
        add_new_search_query(query_str)
        query_obj = YouTubeQuery.objects.get(query=query_str)
        print(query_obj.query)
        print(query_obj.latest.video_id)
        print(query_obj.latest.title)
        print(query_obj.latest.youtube_channel.channel_name)

    @mock.patch("notifier.lib.collect.Collector._goto_query_page")
    def test_collect_new_videos(self, mock_goto_query_page):
        browser = Collector()._setup_browser()  # pylint: disable=W0212
        browser.get(self.live_server_url + "/static/tests/positive.html")
        mock_goto_query_page.return_value = browser

        query = YouTubeQuery(query="hello world")
        channel = YouTubeChannel(
            channel_link="https://example.com",
            channel_name="example",
            channel_img="https://example.com",
        )
        video = YouTubeVideo(
            video_id="wyALgqlfLsk",
            link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            title="Totally not a Rick Roll",
            thumbnail="https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDRxusbm2_TGTnDWEIhBTYW2cUQkw",
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
            print(video.video_id)
