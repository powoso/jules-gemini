from playwright.sync_api import sync_playwright
from app.models import SocialMediaPost
import time
import random

def scrape_twitter_user(username: str):
    """
    Scrapes tweets from a given username using xcancel.com and Playwright.
    """
    posts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            # More realistic browser context
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
                locale="en-US"
            )
            page = context.new_page()

            url = f"https://xcancel.com/{username}"
            print(f"Scraping {url}...")

            try:
                page.goto(url, timeout=30000)

                # Check if we are on the profile page by looking for the user's name or bio
                # Sometimes .timeline-item doesn't load immediately or has a different class
                # XCancel structure might have changed slightly or is loading slowly

                # Try to wait for something more generic first
                try:
                    page.wait_for_selector("body", timeout=5000)
                except:
                    pass

                # Debug: print title
                title = page.title()
                print(f"Page title: {title}")

                # If title indicates error
                if "Error" in title or "404" in title:
                    print(f"Error page detected: {title}")
                    return []

                # Wait for content to load
                try:
                    # timeline-item is the standard class for nitter/xcancel tweets
                    # but let's try a fallback selector if that fails, like .tweet-content
                    page.wait_for_selector(".timeline-item, .tweet-content", timeout=20000)
                except Exception as e:
                    print(f"Timeout waiting for tweets: {e}")
                    # Screenshot for debugging if needed
                    # page.screenshot(path=f"twitter_timeout_{username}.png")
                    return []

                # Scroll a bit to trigger lazy loading if needed
                page.evaluate("window.scrollBy(0, 500)")
                time.sleep(1)

                timeline_items = page.query_selector_all(".timeline-item")
                print(f"Found {len(timeline_items)} timeline items.")

                for item in timeline_items[:10]: # Limit to 10 latest
                    try:
                        # Extract Tweet Content
                        content_div = item.query_selector(".tweet-content")
                        if not content_div:
                            continue
                        content = content_div.inner_text()

                        # Extract Timestamp/Link
                        date_link = item.query_selector(".tweet-date a")
                        if not date_link:
                            continue

                        relative_link = date_link.get_attribute("href")
                        post_url = f"https://xcancel.com{relative_link}" if relative_link else ""

                        # ID is usually the last part of the URL
                        tweet_id = relative_link.split('/')[-1] if relative_link else "unknown"

                        timestamp = date_link.get_attribute("title") # Usually holds the full date

                        # Extract Author
                        fullname_span = item.query_selector(".fullname")
                        author_name = fullname_span.inner_text() if fullname_span else username

                        # Extract Media (Image)
                        media_url = None
                        attachment_img = item.query_selector(".attachment.image img")
                        if attachment_img:
                            src = attachment_img.get_attribute("src")
                            if src:
                                media_url = f"https://xcancel.com{src}" if src.startswith("/") else src

                        # Extract Avatar
                        avatar_url = None
                        avatar_img = item.query_selector(".tweet-avatar img")
                        if avatar_img:
                            src = avatar_img.get_attribute("src")
                            if src:
                                avatar_url = f"https://xcancel.com{src}" if src.startswith("/") else src

                        post = SocialMediaPost(
                            id=tweet_id,
                            source="twitter",
                            author=f"@{username}", # standardized handle
                            content=content,
                            url=post_url,
                            timestamp=timestamp, # We can format this later if needed
                            media_url=media_url,
                            avatar_url=avatar_url
                        )
                        posts.append(post)

                    except Exception as e:
                        print(f"Error parsing tweet item: {e}")
                        continue

            except Exception as e:
                print(f"Error accessing {url}: {e}")

        except Exception as e:
            print(f"Playwright general error: {e}")
        finally:
            browser.close()

    return posts
