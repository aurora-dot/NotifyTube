"""
Collects YouTube video data.
"""

from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=true")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--no-zygote")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
        chrome_options.add_argument("--remote-debugging-port=9222")

        return webdriver.Chrome(options=chrome_options)

    def get_initial_video_for_query(self, search_query) -> list[list, str]:
        browser = self.setup_browser()
        browser.get(
            f"https://www.youtube.com/results?search_query={quote_plus(search_query)}&sp=CAI%253D"
        )

    def _search(self, search_query: str, last_video_id: str) -> list:
        pass

    def _transform_data(self, youtube_list: list, youtube_stats_list: list) -> list:
        pass
