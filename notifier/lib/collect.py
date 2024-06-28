"""
Collects YouTube video data.
"""

import os
from datetime import datetime

import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings
from rfc3339 import rfc3339


class Collector:
    """
    Collects YouTube video data from their API.

    Attributes:
        youtube: a Resource object to interact with Google YouTube API
    """

    def __init__(self) -> None:
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=settings.YOUTUBE_API_KEY
        )
        if settings.DEBUG:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def run(self, search_query, last_datetime):
        """
        Collects video data given a search query and an datetime to collect
        data from *after* the given datetime object

        Args:
            search_query: string, the query to be searched.
            last_datetime: datetime, the datetime to collect data after.

        Returns:
            A list of dictionaries which contain data about the latest vidros.

        Raises:
            ValueError: if the parameters to the function are none or an empty string
        """

        youtube_list = self._search(
            search_query,
            last_datetime,
        )
        stats_list = self._get_video_statistics(youtube_list)

        return self._transform_data(youtube_list, stats_list["items"])

    def _search(self, search_query: str, last_datetime: datetime = None) -> list:
        if search_query in [None, ""]:
            raise ValueError("Parameter search_query cannot be none or empty")

        if last_datetime is None:
            raise ValueError("Parameter last_datetime cannot be none or empty")

        data = []
        next_page_token = None
        initial_run = True

        while next_page_token or initial_run:
            initial_run = False

            request = self.youtube.search().list(  # pylint: disable=E1101
                part="snippet,id",
                maxResults=50,
                order="date",
                q=search_query,
                safeSearch="none",
                publishedAfter=rfc3339(last_datetime),
                pageToken=next_page_token,
            )

            response = request.execute()
            next_page_token = (
                response["nextPageToken"] if "nextPageToken" in response else None
            )

            if response:
                data.append(response)

        return [video for video_data in data for video in video_data["items"]]

    def _get_video_statistics(self, youtube_list: list):
        print(len(youtube_list))

        ids_list = [
            ",".join(
                [video_data["id"]["videoId"] for video_data in youtube_list[i : i + 50]]
            )
            for i in range(0, len(youtube_list), 50)
        ]

        request = self.youtube.videos().list(  # pylint: disable=E1101
            part="id,statistics", id=ids
        )

        return request.execute()

    def _transform_data(self, youtube_list: list, youtube_stats_list: list) -> list:
        data = {}

        for video_data in youtube_list:
            video_data_id = video_data["id"]["videoId"]

            if video_data_id not in data:
                data[video_data_id] = {"video": None, "stats": None}

            if data[video_data_id]["video"]:
                raise ValueError("'video' has a value when it shouldn't have")

            data[video_data_id]["video"] = video_data

        # very similar to loop above, could be turned into a function perhaps
        # you could zip but it makes the code harder to read, just for the sake of
        # saving 50 iterations
        for stats_data in youtube_stats_list:
            stats_data_id = stats_data["id"]

            if data[stats_data_id]["stats"]:
                raise ValueError("'stats' has a value when it shouldn't have")

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
