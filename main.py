from downloader.board_scraper import extract_urls
from downloader.image_downloader import download_image

def run(board_url: str, save_path: str):
    urls, errors = extract_urls(board_url)
    print("error pin:", errors)
    
    download_image(urls[0], save_path, "test1.jpg")

# example
board_url = "https://kr.pinterest.com/flat1000/wallpaper/"
save_path = "d:\test"

run(board_url, save_path)