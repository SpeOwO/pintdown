from downloader.board_scraper import PinterestScraper
from downloader.image_downloader import ImageDownloader
from downloader.utils import sleep

def main():
  board_url = input("write URL of board to download\n")
  save_dir = input("write save directory\n")

  scraper = PinterestScraper()
  scraper.run(board_url)
  url_list, errors = scraper.get_results()

  downloader = ImageDownloader()
  downloader.run(url_list = url_list, save_dir = save_dir, name_fn = lambda url, idx: f"pin_{idx}.jpg")
