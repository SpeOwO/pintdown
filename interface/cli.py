from downloader.board_scraper import extract_urls
from downloader.image_downloader import download_image
from downloader.utils import sleep

def main():
  board_url = input("write URL of board to download\n")
  save_dir = input("write save directory\n")

  urls, errors = extract_urls(board_url)

  for i, url in enumerate(urls):
    filename = str(i)+ ".jpg"
    download_image(url, save_dir, filename)
    sleep()
