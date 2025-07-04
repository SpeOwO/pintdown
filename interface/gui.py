import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import sys

from downloader.board_scraper import PinterestScraper
from downloader.image_downloader import ImageDownloader
from downloader.utils import sleep


# stdout/stderr 리디렉션 클래스
class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)  # 자동 스크롤

    def flush(self):
        pass  # 일부 시스템에서 필요함


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

        # 로그 텍스트창
        tk.Label(root, text="Log:").pack()
        self.log_text = ScrolledText(root, height=15, width=80)
        self.log_text.pack()

        # stdout/stderr을 텍스트창으로 리디렉션
        sys.stdout = RedirectText(self.log_text)
        sys.stderr = RedirectText(self.log_text)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def run_scraper_thread(self):
        # GUI 멈춤 방지를 위한 백그라운드 실행
        threading.Thread(target=self.run_scraper, daemon=True).start()

    def run_scraper(self):
        url = self.url_entry.get()
        path = self.path_entry.get()
        if not url or not path:
            messagebox.showwarning("Input Error", "Please enter both URL and save directory.")
            return

        print(f"\n[INFO] Start scraping: {url}")
        try:
            scraper = PinterestScraper()
            scraper.run(url)
            url_list, error_list = scraper.get_results()

            print(f"[INFO] Collected {len(url_list)} image URLs ({len(error_list)} errors)")

            downloader = ImageDownloader()
            downloader.run(
                url_list=url_list,
                save_dir=path,
                name_fn=lambda url, idx: f"pin_{idx}.jpg"
            )

            print(f"[✔] Done: {len(url_list)} images downloaded.")
            messagebox.showinfo("Done", f"Downloaded {len(url_list)} images.")
        except Exception as e:
            print(f"[✘] Error occurred: {e}")
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = PinterestApp(root)
    root.mainloop()
