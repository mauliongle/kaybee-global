import time
from playwright.sync_api import sync_playwright

def capture_product_cards():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1200})
        
        page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        time.sleep(2)

        out_dir = "C:\\Users\\MAULIINGLE\\.gemini\\antigravity\\brain\\ff77105e-45a5-4a34-afa6-5f57409844e0"

        # Scroll to catalog
        page.locator("#catalog").scroll_into_view_if_needed()
        time.sleep(2)

        # 1. Capture Onions tab
        page.click("button[data-category='onions']")
        time.sleep(1)
        page.screenshot(path=f"{out_dir}\\kaybee_preview_onions_seperate.png")

        # 2. Capture Fruits tab
        page.click("button[data-category='fruits']")
        time.sleep(1)
        page.screenshot(path=f"{out_dir}\\kaybee_preview_fruits_seperate.png")

        browser.close()
        print("Captured individual Onions & Fruits product catalog previews!")

if __name__ == "__main__":
    capture_product_cards()
