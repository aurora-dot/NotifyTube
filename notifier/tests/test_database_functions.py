from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from notifier.lib.database_iterator import add_new_search_query
from notifier.models import YouTubeQuery


class DatabaseFunctionsTestCase(StaticLiveServerTestCase):
    def test_initial_add(self):
        query_str = "test search"
        add_new_search_query(query_str)
        query_obj = YouTubeQuery.objects.get(query=query_str)
        print(query_obj.query)
        print(query_obj.latest.video_id)
        print(query_obj.latest.title)
        print(query_obj.latest.youtube_channel.channel_name)
