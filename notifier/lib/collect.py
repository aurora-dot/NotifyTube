import os
from datetime import datetime

import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings


class Collector:
    def search(self, search_query: str, last_datetime: datetime = None) -> list:
        if settings.DEBUG:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        if search_query in [None, ""]:
            raise ValueError("Parameter search_query is none or empty")

        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=settings.YOUTUBE_API_KEY
        )

        formatted_datetime_string = (
            last_datetime.isoformat("T") if last_datetime else None
        )

        request = youtube.search().list(  # pylint: disable=E1101
            part="snippet,id",
            maxResults=50,
            order="date",
            q="surfing",
            safeSearch="none",
            publishedAfter=formatted_datetime_string,
        )

        response = request.execute()

        return response
