from downloader.board_scraper import PinterestScraper
from downloader.image_downloader import ImageDownloader
from downloader.utils import sleep

def main():
  board_url = input("write URL of board to download\n")
  save_dir = input("write save directory\n")

  scraper = PinterestScraper()
  scraper.run(board_url)
  urls, errors = scraper.get_results()

  downloader = ImageDownloader(save_dir="downloads")