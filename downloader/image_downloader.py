import os
import requests
from . import utils

def download_image(url: str | None, save_dir: str, filename: str = None):
    if not url:
        print(f"[✘] download failure: url is None or empty")
        return

    response = None
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        utils.save_file(response.content, save_dir, filename)
        print(f"[✔] download success: {filename}")

    except Exception as e:
        if response and response.status_code == 403 and "originals" in url:
            fallback_url = url.replace("originals", "1200x")
            print(f"[!] retrying with fallback url: {fallback_url}")
            download_image(fallback_url, save_dir, filename)
        else:
            print(f"[✘] download failure: {url} - {e}")
