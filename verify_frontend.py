from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to frontend...")
            page.goto("http://localhost:8000")

            # Wait for feed container
            page.wait_for_selector("#feed-container")

            # Wait for at least one post to appear (loader hidden)
            page.wait_for_selector("#loader", state="hidden", timeout=30000)

            print("Feed loaded. Taking screenshot...")
            page.screenshot(path="frontend_verification.png", full_page=True)

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="frontend_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_frontend()
