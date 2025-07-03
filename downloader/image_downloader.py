import os
import requests

def download_image(url: str, save_dir: str, filename: str = None):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not filename:
            filename = os.path.basename(url.split("?")[0])  # 쿼리 제거
        save_path = os.path.join(save_dir, filename)

        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"[✔] 다운로드 성공: {filename}")
    except Exception as e:
        print(f"[✘] 다운로드 실패: {url} - {e}")
