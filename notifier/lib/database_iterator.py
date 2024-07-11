"""
Methods which collect and save YouTube videos to store into the database
"""

import traceback
from datetime import datetime

from sentry_sdk import capture_exception

from notifier import models
from notifier.lib.collect import Collector
from notifier.lib.logger import LOGGER

collector = Collector()


def add_new_search_query(search_query):
    """
    Gets the newest YouTube video from a given search query
    Creates a new YouTube objects to save the data into the database

    Args:
        search_query: The query to search for on YouTube
    """
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
    """
    Gets the newest YouTube data for each YouTubeQuery object in the database
    Loops through the newest videos until hitting the
        previous latest video from last call
    Saves the data back into the db and updates the query object with the latest video
    """
    youtube_search_queries = models.YouTubeQuery.objects.all().prefetch_related(
        "latest"
    )

    LOGGER.info("Collector - %s: Started collecting...", datetime.now())

    for search_query in youtube_search_queries:
        videos = []

        try:
            LOGGER.info(
                "Collector - %s: collecting videos for query %s (id: %s), stopping at %s",
                datetime.now(),
                search_query.query,
                search_query.id,
                search_query.latest.video_id,
            )

            collected_videos = collector.get_latest_videos(
                search_query.query, search_query.latest.video_id
            )

            LOGGER.info(
                "Collector - %s: collected videos for query %s (id: %s)",
                datetime.now(),
                search_query.query,
                search_query.id,
            )
        except Exception as error:  # pylint: disable=W0718
            capture_exception(error)
            error_text = f"{datetime.now()}: {error.__class__.__name__} - {error}, Query ID: {search_query.id}, Query Str: '{search_query.query}'"  # pylint: disable=C0301
            traceback_str = traceback.format_exc()
            LOGGER.error(error_text)
            LOGGER.error(traceback_str)

            # skip rest of iteration code
            continue

        LOGGER.info("Collector - %s: Saving data into db...", datetime.now())
        for video in collected_videos:
            channel, _ = models.YouTubeChannel.objects.get_or_create(**video["channel"])
            videos.append(
                models.YouTubeVideo(
                    **video["video"],
                    youtube_query=search_query,
                    youtube_channel=channel,
                )
            )
        models.YouTubeVideo.objects.bulk_create(videos, ignore_conflicts=True)

        newest_video = models.YouTubeVideo.objects.get(video_id=videos[0].video_id)
        search_query.latest = newest_video
        search_query.save()
        LOGGER.info(
            "Collector - %s: Saved into db! Newest video id for query is %s",
            datetime.now(),
            newest_video.video_id,
        )

    LOGGER.info(
        "Collector - %s: Completed collection!",
        datetime.now(),
    )
