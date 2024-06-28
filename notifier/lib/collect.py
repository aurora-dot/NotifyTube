"""
Collects YouTube video data.
"""


class Collector:
    """
    Collects YouTube video data scraped from their webpage.
    """

    def run(self, search_query: str, last_video_id: str) -> list:
        """
        Collects video data given a search query and an previous

        Args:
            search_query: string, the query to be searched.
            last_datetime: datetime, the datetime to collect data after.

        Returns:
            A list of dictionaries which contain data about the latest vidros.

        Raises:
            ValueError: if the parameters to the function are none or an empty string
        """

        pass

    def get_initial_video_to_start_from(self, search_query) -> list[list, str]:
        pass

    def _search(self, search_query: str, last_video_id: str) -> list:
        pass

    def _transform_data(self, youtube_list: list, youtube_stats_list: list) -> list:
        pass
