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

def auto_scroll_until_count(page, scroll_delay=1.5):
    previous_count = 0

    for i in range(max_scrolls):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(scroll_delay)

        current_count = get_loaded_pin_count(page)
        print(f"[{i}] 현재 핀 카드 수: {current_count}")

        # 새 카드가 로드되지 않으면 중단
        if current_count == previous_count:
            print("새로운 핀이 더 이상 로드되지 않음")
            break

        if current_count >= target_count:
            print("요구된 핀 개수만큼 로드 완료")
            break

        previous_count = current_count