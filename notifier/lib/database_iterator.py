from notifier import models
from notifier.lib.collect import Collector

collector = Collector()


def add_new_search_query(self, search_query):
    initial_video = self.collector.get_initial_video_for_query(search_query)

    query = models.YouTubeQuery.objects.get_or_create(query=search_query)
    channel = models.YouTubeChannel.objects.get_or_create(
        channel_link=initial_video["channel"].pop("channel_link"),
        defaults=initial_video["channel"],
    )
    models.YouTubeVideo.objects.get_or_create(
        video_id=initial_video["video"].pop("video_id"),
        defaults=initial_video["video"]
        | {"youtube_query": query, "youtube_channel": channel},
    )


def collect_new_videos(self):
    # get search objects
    youtube_search_queries = models.YouTubeQuery.objects.all().prefetch_related(
        "latest"
    )

    for search_query in youtube_search_queries:
        videos = self.collector.get_latest_videos(
            search_query.query, search_query.latest.video_id
        )

        # for video in videos:
        #     # bulk create using ignore_conflicts
        #     channel = models.YouTubeChannel.objects.get_or_create(
        #         channel_link=initial_video["channel"].pop("channel_link"),
        #         defaults=initial_video["channel"],
        #     )
        #     models.YouTubeVideo.objects.get_or_create(
        #         video_id=initial_video["video"].pop("video_id"),
        #         defaults=initial_video["video"]
        #         | {"youtube_query": query, "youtube_channel": channel},
        #     )
        # add videos to db
        # get newest video id and set it to `search_query.last_video_id`
