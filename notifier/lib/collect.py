"""
Collects YouTube video data.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus

from django.conf import settings
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from notifier.lib.metadata_extractor import MetadataExtractor


class Collector:
    """
    Collects YouTube video data scraped from their webpage.

    Attributes:
        youtube_video_tag: the tag which videos on youtube use
        extractor: to extract the metadata from individual youtube video elements
    """

    youtube_video_tag = "ytd-video-renderer"
    extractor = MetadataExtractor()

    def run(self, search_query: str, last_video_id: str) -> list:
        """
        Collects video data given a search query and an previous video id to stop at

        Args:
            search_query: string, the query to be searched.
            last_video_id: string, the last video id which was captured.

        Returns:
            A list of dictionaries which contain data about the latest videos.

        Raises:
            ValueError: if the parameters to the function are none or an empty string
            LookupError: if the function cannot find the previous video `last_video_id`
            NoSuchElementException: if no element is found
                e.g. no videos under search query
        """
        if not search_query or search_query == "":
            raise ValueError("Nothing in search_query parameter")
        if not last_video_id or last_video_id == "":
            raise ValueError("Nothing in last_video_id parameter")

        return self._get_newest_videos_data(search_query, last_video_id)

    def get_initial_video_for_query(self, search_query) -> list[list, str]:
        """
        Collects the first video data given a search query

        Args:
            search_query: string, the query to be searched.

        Returns:
            A dictionary which contain data about the latest video.

        Raises:
            ValueError: if the parameters to the function are none or an empty string
            NoSuchElementException: if no element is found
                e.g. no videos under search query
        """
        browser = self._goto_query_page(search_query)
        first_video = browser.find_element(By.TAG_NAME, self.youtube_video_tag)
        return self.extractor.extract(first_video)

    def _goto_query_page(self, search_query):
        browser = self._setup_browser()
        browser.get(
            f"https://www.youtube.com/results?search_query={quote_plus(search_query)}&sp=CAI%253D"  # pylint: disable=C0301
        )
        self._close_cookie_popup(browser)

        return browser

    def _search_and_scroll(self, search_query: str, last_video_id: str) -> WebDriver:
        browser = self._goto_query_page(search_query)

        for _ in range(120):
            # currently jank just to get it working,
            # scrolling to body position doesn't work
            browser.execute_script(
                "window.scrollTo(0, 99999999999999999999999999999999)"
            )
            time.sleep(0.5)

            if self._element_exists(
                browser, f'//a[contains(@href ,"{last_video_id}")]'
            ):
                break

            if self._element_exists(
                browser, '//yt-formatted-string[contains(text(), "No more results")]'
            ):
                raise LookupError("Could not find last video id from query")

        if not self._element_exists(
            browser, f'//a[contains(@href ,"{last_video_id}")]'
        ):
            raise LookupError(
                "Could not find last video id from query after all iterations"
            )

        if settings.DEBUG:
            with open("page.html", "w", encoding="utf-8") as file:
                file.write(browser.page_source)

        return browser

    def _get_newest_videos_data(self, search_query: str, last_video_id: str):
        browser = self._search_and_scroll(search_query, last_video_id)
        videos = browser.find_elements(By.TAG_NAME, self.youtube_video_tag)

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.extractor.extract, videos))

        return results

    @staticmethod
    def _element_exists(browser: WebDriver, xpath_string: str):
        try:
            browser.find_element(By.XPATH, xpath_string)
        except NoSuchElementException:
            return False
        return True

    @staticmethod
    def _close_cookie_popup(browser: WebDriver):
        cookie_decline_xpath = '//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button'  # pylint: disable=C0301

        try:
            WebDriverWait(browser, 25).until(
                EC.presence_of_element_located((By.XPATH, cookie_decline_xpath))
            )
        except TimeoutException as error:
            browser.quit()
            raise error

        browser.find_element(By.XPATH, cookie_decline_xpath).click()

    @staticmethod
    def _setup_browser() -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument("--headless=true")

        return Chrome(options=chrome_options)
