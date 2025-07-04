from playwright.sync_api import sync_playwright
import re

def extract_urls(board_url: str):
    image_urls = []
    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(board_url, wait_until="networkidle")

        # 핀 개수 판단
        target_pin_count = get_pin_count(page)
        print(f"[INFO] Target pin count: {target_pin_count}")

        grid_idx = 0
        while len(image_urls) < target_pin_count:
            grid_selector = f'div[data-grid-item-idx="{grid_idx}"]'
            grid_elem = page.locator(grid_selector)

            if grid_elem.count() == 0:
                grid_idx += 1
                continue

            try:
                # scroll to show img
                grid_elem.scroll_into_view_if_needed(timeout=1500)
                pin_card = grid_elem.locator('[aria-label="핀 카드"]')
                if pin_card.count() == 0:
                    # increase target pin count if it is not pin
                    target_pin_count += 1
                    grid_idx += 1
                    continue

                img_locator = pin_card.locator("img")
                if img_locator.count() == 0:
                    errors.append(grid_idx)
                    image_urls.append(None)
                    grid_idx += 1
                    continue

                src = img_locator.get_attribute("src")
                if src and "originals" not in src:
                    src = src.replace("/236x/", "/originals/")
                image_urls.append(src)

            except Exception as e:
                print(f"[ERROR] Grid index {grid_idx}: {e}")
                errors.append(grid_idx)
                image_urls.append(None)

            grid_idx += 1

        browser.close()

    print(f"[RESULT] Collected {len(image_urls) - len(errors)} images with {len(errors)} errors.")
    return image_urls, errors

def get_pin_count(page):
    try:
        pin_count_element = page.locator('div[data-test-id="pin-count"]')
        full_text = pin_count_element.inner_text()
        match = re.search(r'\d+', full_text)
        if match:
            return int(match.group())
    except:
        pass

    print("[WARN] Pin count not found. Fallback to 0.")
    return 0
