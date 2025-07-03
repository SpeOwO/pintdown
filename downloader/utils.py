from playwright.sync_api import sync_playwright
import re

def get_pin_count(page):
  pin_count_element = page.locator('div[data-test-id="pin-count"]')
  # 텍스트 추출
  full_text = pin_count_element.inner_text()
  # 숫자 추출
  match = re.search(r'\d+', full_text)
  if match:
      pin_count = int(match.group())
      print(f"핀 개수: {pin_count}")
  else:
      print("핀 개수를 찾을 수 없습니다.")

  return pin_count