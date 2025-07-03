from playwright.sync_api import sync_playwright
import re

def extract_urls(board_url: str):
    # list to return (image url, the number of error pin)
    image_urls = []
    errors = []

    # run playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # go to url
        page.goto(board_url, wait_until="networkidle")
        
        # get count of pins
        total_pins = get_pin_count(page)

        for i in range(0, total_pins):
          # locator selector
          selector = f'div[data-test-pin-slot-index="{i}"] img'
          try:
              img_locator = page.locator(selector)

              # scroll to locator and set locator on middle of viewport
              img_locator.scroll_into_view_if_needed(timeout=1500)
              page.evaluate("""
                (element) => {
                  const rect = element.getBoundingClientRect();
                  const absoluteElementTop = rect.top + window.pageYOffset;
                  const center = absoluteElementTop - (window.innerHeight / 2) + (rect.height / 2);
                  window.scrollTo({top: center, behavior: 'auto'});
                }
              """, img_locator.element_handle())

              # get url on src
              if img_locator:
                src = img_locator.get_attribute("src")
                if src and "originals" not in src:
                    src = src.replace("/236x/", "/originals/")
                image_urls.append(src)
              
              # no locator
              else:
                errors.append(i)
                image_urls.append(None)

          except Exception as e:
              print(f"Error at pin index {i}: {e}")
              errors.append(i)
              image_urls.append(None)

        # close
        browser.close()
    
    print(total_pins-errors, " success of", total_pins)
    return image_urls, errors

def get_pin_count(page):
  pin_count_element = page.locator('div[data-test-id="pin-count"]')
  # extract text
  full_text = pin_count_element.inner_text()
  # extract number
  match = re.search(r'\d+', full_text)
  if match:
      pin_count = int(match.group())
      print(f"count of pins: {pin_count}")
  else:
      print("pin count not found")

  return pin_count