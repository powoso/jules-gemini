from playwright.sync_api import sync_playwright

def test_reddit_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://www.reddit.com/r/technology/")
            print(f"Reddit Page Title: {page.title()}")

            # Wait for content to load
            page.wait_for_selector("shreddit-post", timeout=10000)

            posts = page.query_selector_all("shreddit-post")
            print(f"Found {len(posts)} posts")

            for i, post in enumerate(posts[:5]):
                title = post.get_attribute("post-title")
                print(f" - {title}")

        except Exception as e:
            print(f"Reddit Playwright Error: {e}")
        finally:
            browser.close()

test_reddit_playwright()
