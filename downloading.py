import requests
import time

urls = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

for url in urls:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"{filename} 다운로드 완료")
    else:
        print(f"{url} 다운로드 실패, 상태 코드: {response.status_code}")

    time.sleep(2)  # 2초 쉬기