from playwright.sync_api import sync_playwright, Page
import re
import logging

logger = logging.getLogger("pintdown.scraper")

class PinterestScraper:
    def __init__(self):
        self.board_url = None
        self.image_urls = []
        self.errors = []
        self.target_pin_count = 0
        self.grid_idx = 0

    def reset(self):
        self.board_url = None
        self.image_urls.clear()
        self.errors.clear()
        self.target_pin_count = 0
        self.grid_idx = 0

    def run(self, board_url: str):
        self.reset()
        self.board_url = board_url
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.board_url, wait_until="networkidle")

            self.original_pin_count = self.get_pin_count(page)
            self.target_pin_count = self.original_pin_count
            logger.info(f"found {self.target_pin_count} pins")

            last_result = None
            while len(self.image_urls) < self.original_pin_count:
                result, src = self.process_grid_item(page, self.grid_idx)
                self.handle_result(result, src)
                if result == 'not_loaded' and last_result == 'not_loaded':
                    break
                last_result = result
                self.grid_idx += 1

            browser.close()

    def get_pin_count(self, page: Page) -> int:
        try:
            pin_count_element = page.locator('div[data-test-id="pin-count"]')
            full_text = pin_count_element.inner_text()
            match = re.search(r'\d+', full_text)
            if match:
                return int(match.group())
        except Exception as e:
            logger.warning(f"Could not get pin count: {e}")

        logger.warning("Pin count not found. Fallback to 0.")
        return 0

    def process_grid_item(self, page: Page, grid_idx: int):
        grid_selector = f'div[data-grid-item-idx="{grid_idx}"]'
        grid_elem = page.locator(grid_selector)

        if grid_elem.count() == 0:
            logger.debug(f"Grid index {grid_idx} not loaded yet.")
            return "not_loaded", None

        try:
            grid_elem.scroll_into_view_if_needed(timeout=1500)
            logger.debug(f"Scrolled into view: grid index {grid_idx}")

            pin_card = grid_elem.locator('[data-test-id="pin"]')
            if pin_card.count() == 0:
                logger.debug(f"No pin found at grid index {grid_idx}")
                return "not_pin", None

            img_locator = pin_card.locator("img")
            if img_locator.count() == 0:
                logger.debug(f"No image tag found at grid index {grid_idx}")
                return "error", None

            src = img_locator.get_attribute("src")
            if not src:
                logger.debug(f"Image src is empty at grid index {grid_idx}")
                return "error", None

            # Replace low-res with high-res if needed
            src = src.replace("/236x/", "/originals/")

            return "success", src

        except Exception as e:
            logger.error(f"Exception at grid index {grid_idx}: {e}")
            return "error", None

    def handle_result(self, result: str, src: str | None):
        if result == "not_pin":
            self.target_pin_count += 1
            logger.info(f"Grid index {self.grid_idx} is not a pin. Increasing target_pin_count to {self.target_pin_count}")
        elif result == "error":
            self.errors.append(self.grid_idx)
            self.image_urls.append(None)
            logger.error(f"Error at grid index {self.grid_idx}. Added to errors.")
        elif result == "success":
            self.image_urls.append(src)
            logger.info(f"Successfully retrieved image URL at grid index {self.grid_idx}")

    def get_results(self):
        return self.image_urls, self.errors
