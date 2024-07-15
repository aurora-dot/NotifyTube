"""
Collects YouTube video data.
"""

import time
from datetime import datetime
from urllib.parse import quote_plus

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from notifier.lib.logger import LOGGER
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
    url_parameter_for_ordering_by_latest = "sp=CAI%253D"

    def get_latest_videos(
        self, search_query: str, latest_video_ids: str, max_scrolls: int = 25
    ) -> list[dict]:
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
        if not latest_video_ids or latest_video_ids == "" or latest_video_ids == []:
            raise ValueError("Nothing in last_video_id parameter")

        return self._search_scroll_extract(search_query, latest_video_ids, max_scrolls)

    def get_initial_video_for_query(self, search_query: str) -> dict:
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
        if not search_query or search_query == "":
            raise ValueError("Nothing in search_query parameter")

        browser = self._goto_query_page(search_query)
        videos = browser.find_elements(By.TAG_NAME, self.youtube_video_tag)
        extracted = []
        for video in videos:
            ActionChains(browser).move_to_element(video).perform()
            extracted.append(self.extractor.extract(video))
        return extracted

    def _goto_query_page(self, search_query: str) -> WebDriver:
        browser = self._setup_browser()
        browser.get(
            f"https://www.youtube.com/results?search_query={quote_plus(search_query)}&{self.url_parameter_for_ordering_by_latest}"  # pylint: disable=C0301
        )
        # time.sleep(10)
        # print("----- screenshot start -----\n\n")
        # print(browser.get_screenshot_as_base64())
        # print("----- screenshot end -----\n\n")

        # self._close_cookie_popup(browser)

        return browser

    def _search_scroll_extract(
        self, search_query: str, latest_video_ids: list, max_scrolls: int
    ) -> list[dict]:
        browser = self._goto_query_page(search_query)

        loop_start = 0
        current_scrolls = 0
        videos = []

        while current_scrolls <= max_scrolls:
            LOGGER.info(
                "Collector - %s: scroll %s/%s for query '%s'",
                datetime.now(),
                current_scrolls,
                max_scrolls,
                search_query,
            )
            video_elements = browser.find_elements(By.TAG_NAME, self.youtube_video_tag)
            for i in range(loop_start, len(video_elements)):
                ActionChains(browser).move_to_element(video_elements[i]).perform()
                extracted = self.extractor.extract(video_elements[i])
                if extracted["video"]["video_id"] in latest_video_ids:
                    break
                LOGGER.info(
                    "Collector - %s: found video '%s' for query '%s'",
                    datetime.now(),
                    extracted["video"]["video_id"],
                    search_query,
                )
                videos.append(extracted)

            if self._element_exists(
                browser, '//yt-formatted-string[contains(text(), "No more results")]'
            ):
                raise LookupError("Could not find last video id from query")

            if self._video_is_on_page(browser, latest_video_ids):
                break

            loop_start = len(video_elements)

            # Scroll to bottom to trigger new reload
            browser.execute_script(
                "window.scrollTo(0, 99999999999999999999999999999999)"
            )

            current_scrolls += 1

            time.sleep(1)

        # latter half of bool statement is just in case on the last scroll it is found
        if current_scrolls >= max_scrolls and not self._video_is_on_page(
            browser, latest_video_ids
        ):
            raise LookupError(
                f"Could not find the previous video in {current_scrolls} page scrolls"
            )

        return videos

    def _video_is_on_page(self, browser, latest_video_ids):
        return any(
            [
                self._element_exists(browser, f'//a[contains(@href ,"{video_id}")]')
                for video_id in latest_video_ids
            ]
        )

    @staticmethod
    def _element_exists(browser: WebDriver, xpath_string: str) -> bool:
        try:
            browser.find_element(By.XPATH, xpath_string)
        except NoSuchElementException:
            return False
        return True

    @staticmethod
    def _close_cookie_popup(browser: WebDriver):
        cookie_decline_xpath = '//span[contains(text(), "Reject all")]'

        try:
            WebDriverWait(browser, 25).until(
                EC.presence_of_element_located((By.XPATH, cookie_decline_xpath))
            )
        except TimeoutException as error:
            browser.quit()
            raise error

        ActionChains(browser).click(
            browser.find_element(By.XPATH, cookie_decline_xpath)
        ).perform()

    @staticmethod
    def _setup_browser() -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--headless=true")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"  # pylint: disable=C0301
        )

        return Chrome(options=chrome_options)
