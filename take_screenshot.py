import time
from playwright.sync_api import sync_playwright

def capture_preview():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        print("Navigating to http://127.0.0.1:5000...")
        page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        time.sleep(3) # allow Three.js globe to render

        out_dir = "C:\\Users\\MAULIINGLE\\.gemini\\antigravity\\brain\\ff77105e-45a5-4a34-afa6-5f57409844e0"

        # 1. Hero Section
        page.screenshot(path=f"{out_dir}\\kaybee_preview_hero.png")
        print("Captured Hero Preview")

        # 2. 3D Globe Section
        globe_section = page.locator("#trade-globe-section")
        globe_section.scroll_into_view_if_needed()
        time.sleep(2)
        page.screenshot(path=f"{out_dir}\\kaybee_preview_globe.png")
        print("Captured Globe Preview")

        # 3. Catalog Section
        catalog_section = page.locator("#catalog")
        catalog_section.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=f"{out_dir}\\kaybee_preview_catalog.png")
        print("Captured Catalog Preview")

        # 4. RFQ Section
        rfq_section = page.locator("#rfq-calculator")
        rfq_section.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=f"{out_dir}\\kaybee_preview_rfq.png")
        print("Captured RFQ Preview")

        # 5. Payment Modal
        page.evaluate("openPaymentGatewayModal('card')")
        time.sleep(1)
        page.screenshot(path=f"{out_dir}\\kaybee_preview_payment.png")
        print("Captured Payment Modal Preview")

        browser.close()
        print("All Screenshots Captured Successfully!")

if __name__ == "__main__":
    capture_preview()
