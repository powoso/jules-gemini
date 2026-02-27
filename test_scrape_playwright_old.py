from playwright.sync_api import sync_playwright

def test_reddit_playwright_old():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://old.reddit.com/r/technology/")
            print(f"Old Reddit Page Title: {page.title()}")

            # Wait for content to load
            page.wait_for_selector("div.thing", timeout=10000)

            posts = page.query_selector_all("div.thing a.title")
            print(f"Found {len(posts)} posts")

            for i, post in enumerate(posts[:5]):
                print(f" - {post.inner_text()}")

        except Exception as e:
            print(f"Old Reddit Playwright Error: {e}")
        finally:
            browser.close()

test_reddit_playwright_old()
