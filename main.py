from downloader.board_scraper import extract_urls
from downloader.image_downloader import download_image
from downloader.utils import sleep

def run(board_url: str, save_path: str):
    urls, errors = extract_urls(board_url)
    print("error pin:", errors)

    for i, url in enumerate(urls):
        file_name = str(i + 1) + ".jpg"
        download_image(url, save_path, file_name)
        sleep()

if __name__ == '__main__':
    # example
    board_url = "https://kr.pinterest.com/flat1000/wallpaper/"
    save_path = "d:/test"
    download_image("https://i.pinimg.com/originals/dc/ae/57/dcae57655cff2f15584d325a80c1edbb.jpg", "c:/test", "test3.jpg")
    #run(board_url, save_path)