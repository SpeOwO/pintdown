import asyncio
from playwright.async_api import async_playwright

# 로그인 정보 입력
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

async def login_to_pinterest():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # GUI로 보려면 headless=False
        context = await browser.new_context()
        page = await context.new_page()

        # Pinterest 로그인 페이지로 이동
        await page.goto("https://www.pinterest.com/login/")

        # 이메일 입력
        await page.fill('input[name="id"]', EMAIL)

        # 비밀번호 입력
        await page.fill('input[name="password"]', PASSWORD)

        # 로그인 버튼 클릭
        await page.click('button[type="submit"]')

        # 로그인 완료 대기 (예: 홈피드가 보일 때까지)
        await page.wait_for_url("https://www.pinterest.com/*", timeout=10000)

        print("✅ 로그인 완료")

        # 10초간 브라우저 열린 상태 유지 (테스트용)
        await asyncio.sleep(10)

        await browser.close()

# 실행
asyncio.run(login_to_pinterest())
