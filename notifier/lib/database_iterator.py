from notifier import models
from notifier.lib.collect import Collector

collector = Collector()


def add_new_search_query(search_query):
    initial_video = collector.get_initial_video_for_query(search_query)

    query, _ = models.YouTubeQuery.objects.get_or_create(query=search_query)
    channel, _ = models.YouTubeChannel.objects.get_or_create(
        channel_link=initial_video["channel"].pop("channel_link"),
        defaults=initial_video["channel"],
    )
    video, _ = models.YouTubeVideo.objects.get_or_create(
        video_id=initial_video["video"].pop("video_id"),
        defaults=initial_video["video"]
        | {"youtube_query": query, "youtube_channel": channel},
    )

    query.latest = video
    query.save()


def collect_new_videos():
    # get search objects
    youtube_search_queries = models.YouTubeQuery.objects.all().prefetch_related(
        "latest"
    )

    videos = []

    for search_query in youtube_search_queries:
        collected_videos = collector.get_latest_videos(
            search_query.query, search_query.latest.video_id
        )

        videos[search_query.query] = []

        # this needs to be a bulk insert
        for video in collected_videos:
            channel, _ = models.YouTubeChannel.objects.get_or_create(
                channel_link=video["channel"].pop("channel_link"),
                defaults=video["channel"],
            )
            videos[search_query.query].append(
                models.YouTubeVideo.objects.get_or_create(
                    video_id=video["video"].pop("video_id"),
                    defaults=video["video"]
                    | {"youtube_query": search_query, "youtube_channel": channel},
                )[0]
            )

        search_query.latest = videos[search_query.query][0]
        search_query.save()
