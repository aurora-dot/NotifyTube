"""
Collects YouTube video data.
"""

import time
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

    def _setup_browser(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless=true")
        # chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-setuid-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-dev-tools")
        # chrome_options.add_argument("--no-zygote")
        # chrome_options.add_argument("--single-process")
        # chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
        # chrome_options.add_argument("--remote-debugging-port=9222")

        return webdriver.Chrome(options=chrome_options)

    def get_initial_video_for_query(self, search_query) -> list[list, str]:
        pass

    def _search(self, search_query: str, last_video_id: str) -> list:
        browser = self._setup_browser()
        browser.get(
            f"https://www.youtube.com/results?search_query={quote_plus(search_query)}&sp=CAI%253D"
        )
        cookie_decline_xpath = '//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button'

        try:
            WebDriverWait(browser, 25).until(
                EC.presence_of_element_located((By.XPATH, cookie_decline_xpath))
            )
        except TimeoutException as error:
            browser.quit()
            raise error

        browser.find_element(By.XPATH, cookie_decline_xpath).click()
        time.sleep(1)

        # this should be dynamic, scrolling the the previous video id and stopping when it hits it
        for _ in range(60):
            # currently jank just to get it working, scrolling to body position doesn't work
            browser.execute_script(
                "window.scrollTo(0, 99999999999999999999999999999999)"
            )
            time.sleep(0.5)

            # if //*[@id="message"] appears, we have reached bottom

        with open("page.html", "w", encoding="utf-8") as file:
            file.write(browser.page_source)

    def _transform_data(self, youtube_list: list, youtube_stats_list: list) -> list:
        pass
