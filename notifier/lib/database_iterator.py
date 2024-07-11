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
    youtube_search_queries = models.YouTubeQuery.objects.all().prefetch_related(
        "latest"
    )

    for search_query in youtube_search_queries:
        videos = []
        collected_videos = collector.get_latest_videos(
            search_query.query, search_query.latest.video_id
        )

        for video in collected_videos:
            channel, _ = models.YouTubeChannel.objects.get_or_create(**video["channel"])
            videos.append(
                models.YouTubeVideo(
                    **video["video"],
                    youtube_query=search_query,
                    youtube_channel=channel
                )
            )
        models.YouTubeVideo.objects.bulk_create(videos, ignore_conflicts=True)

        search_query.latest = models.YouTubeVideo.objects.get(
            video_id=videos[0].video_id
        )
        search_query.save()
