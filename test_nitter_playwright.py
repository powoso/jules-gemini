from playwright.sync_api import sync_playwright

def test_nitter_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to nitter.aosus.link...")
            page.goto("https://nitter.aosus.link/elonmusk")
            print(f"Page Title: {page.title()}")

            # Wait for tweets
            try:
                page.wait_for_selector(".timeline-item", timeout=10000)
                print("Timeline items found!")
                tweets = page.query_selector_all(".timeline-item .tweet-content")
                for i, tweet in enumerate(tweets[:3]):
                    print(f" - {tweet.inner_text()[:50]}...")
            except:
                print("Timeout waiting for timeline items.")
                print(f"Content: {page.content()[:500]}")

        except Exception as e:
            print(f"Playwright Error: {e}")
        finally:
            browser.close()

test_nitter_playwright()
