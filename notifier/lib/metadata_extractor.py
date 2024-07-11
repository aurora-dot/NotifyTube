"""
Extracts data from youtube video elements
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class MetadataExtractor:
    """
    Extracts data from youtube video elements for storage of mass data
    """

    def extract(self, video_element: WebElement):
        """
        Extracts data from youtube element and returns a dictonary of
        data

        Args:
            video_element: WebElement, for extraction of youtube video data
        """

        return {
            "video": self._get_link_data(video_element)
            | self._get_title_and_thumbnail(video_element),
            "channel": self._get_channel_data(video_element),
        }

    def _get_title_and_thumbnail(self, video_element):
        title = (
            video_element.find_element(By.ID, "video-title")
            .find_element(By.TAG_NAME, "yt-formatted-string")
            .text
        )
        thumbnail = (
            video_element.find_element(By.TAG_NAME, "ytd-thumbnail")
            .find_element(By.TAG_NAME, "yt-image")
            .find_element(By.TAG_NAME, "img")
            .get_attribute("src")
        )

        return {"title": title, "thumbnail": thumbnail}

    def _get_link_data(self, video_element):
        normal_url_prefix = "https://www.youtube.com/watch?v="
        shorts_url_prefix = "https://www.youtube.com/shorts/"

        dirty_link = video_element.find_element(By.ID, "thumbnail").get_attribute(
            "href"
        )
        cleaned_link = dirty_link.split("&", 1)[0]
        first_pass = cleaned_link.removeprefix(normal_url_prefix)
        video_id = first_pass.removeprefix(shorts_url_prefix)

        if normal_url_prefix in video_id or shorts_url_prefix in video_id:
            raise ValueError("video_id still contains url prefix")

        return {"video_id": video_id, "link": cleaned_link}

    def _get_channel_data(self, video_element):
        channel_img = video_element.find_element(By.ID, "img").get_attribute("src")
        channel_name_element = video_element.find_element(
            By.ID, "channel-name"
        ).find_element(By.TAG_NAME, "a")
        channel_name = channel_name_element.get_property("innerText")
        channel_link = channel_name_element.get_attribute("href")

        return {
            "channel_link": channel_link,
            "channel_name": channel_name,
            "channel_img": channel_img,
        }
