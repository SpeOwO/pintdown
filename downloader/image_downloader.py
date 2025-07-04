import requests
import logging
from . import utils

logger = logging.getLogger("pintdown.downloader")

class ImageDownloader:
    def __init__(self, timeout: int = 10):
        """
        :param timeout: request timeout in seconds
        """
        self.save_dir = None
        self.timeout = timeout
    
    def reset(self):
        self.save_dir = None

    def download(self, url: str | None, filename: str = None):
        """
        Download an image from the URL and save it.
        Retries with a fallback URL if 403 error occurs on original URL.
        """
        response = None
        if not url:
            logger.warning(f"Skipping download: URL is None or empty (filename={filename})")
            return

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if response and response.status_code == 403 and "originals" in url:
                fallback_url = url.replace("originals", "1200x")
                logger.info(f"Retrying with fallback URL: {fallback_url}")
                self.download(fallback_url, filename)
            else:
                logger.error(f"Request failed: {url} - {e}")
            return

        try:
            utils.save_file(response.content, self.save_dir, filename)
            logger.info(f"Download success: {filename}")
        except Exception as e:
            logger.error(f"File save failed: {filename} - {e}")

    def run(self, url_list: list[str | None], save_dir: str, name_fn=None, progress_callback=None):
        self.reset()
        self.save_dir = save_dir
        total = len(url_list)
        for idx, url in enumerate(url_list):
            if not url:
                logger.warning(f"Skipping invalid URL at index {idx}")
                continue
            filename = name_fn(url, idx) if name_fn else None
            self.download(url, filename)
            
            if progress_callback:
                progress_callback(idx + 1, total)

            if idx < total - 1: 
                utils.sleep()
