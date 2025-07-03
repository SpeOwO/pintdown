import os
import requests
import utils

def download_image(url: str, save_dir: str, filename: str = None):
    try:
        # url에 리퀘스트 요청
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # 파일 저장
        utils.save_file(response.content, save_dir, filename)
        print(f"[✔] 다운로드 성공: {filename}")
    except Exception as e:
        print(f"[✘] 다운로드 실패: {url} - {e}")
