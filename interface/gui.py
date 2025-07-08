import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading
import logging
import sys
import time
import os
import json
from urllib.parse import urlparse

from downloader.board_scraper import PinterestScraper
from downloader.image_downloader import ImageDownloader


# ----------------------------
# Logging Handler for Tkinter
# ----------------------------
class TextHandler(logging.Handler):
    """Custom logging handler to write logs to a Tkinter text widget."""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, self.append_text, msg + "\n")

    def append_text(self, msg):
        self.text_widget.insert(tk.END, msg)
        self.text_widget.see(tk.END)


# ----------------------------
# Filename Generation Functions
# ----------------------------

def name_by_index(url: str, idx: int) -> str:
    return f"{idx + 1}.jpg"

def name_by_timestamp(url: str, idx: int) -> str:
    return f"{int(time.time() * 1000)}.jpg"

def name_by_original(url: str, idx: int) -> str:
    try:
        path = urlparse(url).path
        filename = os.path.basename(path)
        return filename or f"image_{idx + 1}.jpg"
    except:
        return f"image_{idx + 1}.jpg"


# ----------------------------
# Main GUI Application Class
# ----------------------------
class PinterestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pinterest Image Downloader")

        self.naming_options = {
            "Numbered (1.jpg, 2.jpg)": name_by_index,
            "Timestamp": name_by_timestamp,
            "Original filename": name_by_original,
        }
        self.name_fn = name_by_index  # default
        self.settings_path = "settings.json"
        self.load_settings()

        # URL input
        tk.Label(root, text="Pinterest Board URL:").pack()
        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.pack()

        # Save path input
        tk.Label(root, text="Save Directory:").pack()
        self.path_entry = tk.Entry(root, width=60)
        self.path_entry.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Browse...", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Settings", command=self.open_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Run", command=self.run_scraper_thread).pack(side=tk.LEFT, padx=5)
        
        # Progress bar and labels
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(root, length=400, variable=self.progress_var, maximum=100)
        self.progress_bar.pack()

        self.progress_label = tk.Label(root, text="0% complete")
        self.progress_label.pack()

        self.time_label = tk.Label(root, text="Estimated time left: --:--")
        self.time_label.pack()

        # Log window
        tk.Label(root, text="Log:").pack()
        self.log_text = ScrolledText(root, height=15, width=80, state='normal')
        self.log_text.pack()

        # Logger setup
        self.logger = logging.getLogger("pintdown")
        self.logger.setLevel(logging.DEBUG)

        gui_handler = TextHandler(self.log_text)
        gui_handler.setLevel(logging.INFO)
        gui_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(gui_handler)
        self.logger.addHandler(console_handler)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)

    def update_progress(self, current, total):
        percent = int((current / total) * 100)
        self.progress_var.set(percent)
        self.progress_label.config(text=f"{percent}% complete")

        eta_seconds = (total - current) * 0.75
        minutes = int(eta_seconds // 60)
        seconds = int(eta_seconds % 60)
        self.time_label.config(text=f"Estimated time left: {minutes:02d}:{seconds:02d}")

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
                name_fn=self.name_fn,
                progress_callback=self.update_progress
            )

            self.logger.info(f"Done: {len(url_list)} images downloaded.")
            messagebox.showinfo("Done", f"Downloaded {len(url_list)} images.")
        
            # Save settings
            self.save_settings()

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            messagebox.showerror("Error", str(e))

    def open_settings(self):
        """Open a settings window for selecting filename strategy."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("350x200")

        tk.Label(settings_window, text="Select Filename Strategy:").pack(pady=10)

        var = tk.StringVar(value=self.current_setting_name())

        def set_and_close():
            self.name_fn = self.naming_options.get(var.get(), name_by_index)
            self.save_settings()
            settings_window.destroy()

        for name in self.naming_options.keys():
            tk.Radiobutton(settings_window, text=name, variable=var, value=name).pack(anchor="w", padx=20)

        tk.Button(settings_window, text="Apply", command=set_and_close).pack(pady=10)

    def save_settings(self):
        try:
            setting_name = self.current_setting_name()
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump({"filename_strategy": setting_name}, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Failed to save settings.json: {e}")

    def load_settings(self):
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    strategy = data.get("filename_strategy")
                    if strategy in self.naming_options:
                        self.name_fn = self.naming_options[strategy]
        except Exception as e:
            self.logger.warning(f"Failed to load settings.json: {e}")

    def current_setting_name(self):
        for name, fn in self.naming_options.items():
            if fn == self.name_fn:
                return name
        return list(self.naming_options.keys())[0]


# ----------------------------
# App Entry Point
# ----------------------------
def main():
    root = tk.Tk()
    app = PinterestApp(root)
    root.mainloop()
