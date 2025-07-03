import os
import requests
from . import utils

def download_image(url: str, save_dir: str, filename: str = None):
    try:
        # request on url
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # save content as a file
        utils.save_file(response.content, save_dir, filename)
        print(f"[✔] download succes: {filename}")
    except Exception as e:
        print(f"[✘] download failure: {url} - {e}")
