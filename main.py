from downloader.board_scraper import extract_urls

# ��� ����
board_url = "https://kr.pinterest.com/flat1000/wallpaper/"

urls, errors = extract_urls(board_url)
for idx, url in enumerate(urls, 1):
    print(f"{idx}: {url}")
print(len(urls)-len(errors),"�� ����")

def run(board_url: str, save_path: str):
    extract_urls(board_url)
