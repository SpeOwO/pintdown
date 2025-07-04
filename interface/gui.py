import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading
import logging
import sys

from downloader.board_scraper import PinterestScraper
from downloader.image_downloader import ImageDownloader
from downloader.utils import sleep

# logging 핸들러: 로그 메시지를 Tkinter 텍스트 위젯에 출력
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        # GUI 스레드에서 안전하게 UI 업데이트
        self.text_widget.after(0, self.append_text, msg + "\n")

    def append_text(self, msg):
        self.text_widget.insert(tk.END, msg)
        self.text_widget.see(tk.END)  # 자동 스크롤


class PinterestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pinterest Image Downloader")

        # URL 입력
        tk.Label(root, text="Pinterest Board URL:").pack()
        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.pack()

        # 저장 경로 입력
        tk.Label(root, text="Save Directory:").pack()
        self.path_entry = tk.Entry(root, width=60)
        self.path_entry.pack()

        # 버튼
        tk.Button(root, text="Browse...", command=self.browse_folder).pack()
        tk.Button(root, text="Run", command=self.run_scraper_thread).pack()

        # Progress bar
        tk.Label(root, text="Progress:").pack()
        self.progress = tk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack()

        # 로그 텍스트창
        tk.Label(root, text="Log:").pack()
        self.log_text = ScrolledText(root, height=15, width=80, state='normal')
        self.log_text.pack()

        # 로거 세팅
        self.logger = logging.getLogger("pintdown")
        self.logger.setLevel(logging.DEBUG)

        # GUI 핸들러 (INFO 이상만 출력)
        gui_handler = TextHandler(self.log_text)
        gui_handler.setLevel(logging.INFO)
        gui_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        gui_handler.setFormatter(gui_formatter)

        # 콘솔 핸들러 (DEBUG 이상 모두 출력)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)

        # 중복 핸들러 방지
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(gui_handler)
        self.logger.addHandler(console_handler)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def run_scraper_thread(self):
        threading.Thread(target=self.run_scraper, daemon=True).start()

    def run_scraper(self):
        url = self.url_entry.get()
        path = self.path_entry.get()
        if not url or not path:
            messagebox.showwarning("Input Error", "Please enter both URL and save directory.")
            return

        self.logger.info(f"Start scraping: {url}")
        try:
            scraper = PinterestScraper()
            scraper.run(url)
            url_list, error_list = scraper.get_results()

            self.logger.info(f"Collected {len(url_list)} image URLs ({len(error_list)} errors)")

            downloader = ImageDownloader()
            downloader.run(
                url_list=url_list,
                save_dir=path,
                name_fn=lambda url, idx: f"pin_{idx}.jpg"
            )

            self.logger.info(f"Done: {len(url_list)} images downloaded.")
            messagebox.showinfo("Done", f"Downloaded {len(url_list)} images.")
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = PinterestApp(root)
    root.mainloop()
