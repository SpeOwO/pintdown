from playwright.sync_api import sync_playwright
import re

def extract_urls(board_url: str):
    # 반환할 리스트 (image url, error 발생한 번호)
    image_urls = []
    errors = []

    # playwright 실행
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # url 이동
        page.goto(board_url, wait_until="networkidle")
        
        # url 내 핀 개수 확인
        total_pins = get_pin_count(page)

        for i in range(0, total_pins):
          
          # 핀 인덱스 번호로 핀 로케이터 셀렉트
          selector = f'div[data-test-pin-slot-index="{i}"] img'
          try:
              img_locator = page.locator(selector)

              # 로케이터 추적 + 화면 중앙으로 이동
              img_locator.scroll_into_view_if_needed(timeout=1500)
              page.evaluate("""
                (element) => {
                  const rect = element.getBoundingClientRect();
                  const absoluteElementTop = rect.top + window.pageYOffset;
                  const center = absoluteElementTop - (window.innerHeight / 2) + (rect.height / 2);
                  window.scrollTo({top: center, behavior: 'auto'});
                }
              """, img_locator.element_handle())

              # img element 중 src에 'originals' 포함된 url 얻기
              if img_locator:
                src = img_locator.get_attribute("src")
                if src and "originals" not in src:
                    src = src.replace("/236x/", "/originals/")
                image_urls.append(src)
              
              # locator 존재하지 않음
              else:
                errors.append(i)
                image_urls.append(None)

          except Exception as e:
              print(f"Error at pin index {i}: {e}")
              errors.append(i)
              image_urls.append(None)

        # 브라우저 종료
        browser.close()
    
    print(total_pins, "중 ", total_pins-errors, "개 성공")
    return image_urls, errors

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