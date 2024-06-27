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
