import os
from datetime import datetime

import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings
from rfc3339 import rfc3339


class Collector:
    def __init__(self) -> None:
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=settings.YOUTUBE_API_KEY
        )
        if settings.DEBUG:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def search(self, search_query: str, last_datetime: datetime = None) -> list:
        if search_query in [None, ""]:
            raise ValueError("Parameter search_query is none or empty")

        formatted_datetime_string = rfc3339(last_datetime) if last_datetime else None

        request = self.youtube.search().list(  # pylint: disable=E1101
            part="snippet,id",
            maxResults=50,
            order="date",
            q="surfing",
            safeSearch="none",
            publishedAfter=formatted_datetime_string,
        )

        response = request.execute()

        return response

    def get_video_statistics(self, youtube_list: list):
        ids = ",".join([video_data["id"]["videoId"] for video_data in youtube_list])

        request = self.youtube.videos().list(  # pylint: disable=E1101
            part="id,statistics", id=ids
        )

        response = request.execute()

        return response

    def transform_data(self, youtube_list: list, youtube_stats_list: list) -> list:
        data = {}

        for video_data in youtube_list:
            video_data_id = video_data["id"]["videoId"]

            if video_data_id not in data:
                data[video_data_id] = {"video": None, "stats": None}

            if data[video_data_id]["video"]:
                raise ValueError("video has a value where there should be none")

            data[video_data_id]["video"] = video_data

        # very similar to loop above, could be turned into a function perhaps
        for stats_data in youtube_stats_list:
            stats_data_id = stats_data["id"]

            if data[stats_data_id]["stats"]:
                raise ValueError("video has a value where there should be none")

            data[stats_data_id]["stats"] = stats_data

        return [
            {
                "video_id": video_data["video"]["id"]["videoId"],
                "channel_title": video_data["video"]["snippet"]["channelTitle"],
                "channel_id": video_data["video"]["snippet"]["channelId"],
                "title": video_data["video"]["snippet"]["title"],
                "thumbnail": video_data["video"]["snippet"]["thumbnails"]["high"][
                    "url"
                ],
                "publish_time": video_data["video"]["snippet"]["publishedAt"],
                "views": video_data["stats"]["statistics"]["viewCount"],
            }
            for video_data in data.values()
        ]
