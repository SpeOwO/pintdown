import os
import requests
from . import utils

def download_image(url: str, save_dir: str, filename: str = None):
    if url == None:
        print(f"[✘] download failure: {url} - {e}")
        return

    try:
        # request on url
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # save content as a file
        utils.save_file(response.content, save_dir, filename)
        print(f"[✔] download succes: {filename}")
        
    except Exception as e:
        if response and response.status_code == 403 and "originals" in url:
            url = url.replace("originals", "1200x")
            download_image(url, save_dir, filename)
        else:
            print(f"[✘] download failure: {url} - {e}")