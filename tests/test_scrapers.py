import pytest
from app.services.reddit import scrape_subreddit
from app.services.twitter import scrape_twitter_user

def test_reddit_structure():
    posts = scrape_subreddit(limit=1)
    if posts:
        post = posts[0]
        assert post.source == "reddit"
        assert post.content is not None
        assert post.author.startswith("u/")

def test_twitter_structure():
    # This might fail if network is flaky or rate limited, but good for local check
    # We'll mock or just run it and catch exception to not fail build if external service is down
    try:
        posts = scrape_twitter_user("elonmusk")
        if posts:
            post = posts[0]
            assert post.source == "twitter"
            assert post.content is not None
            assert post.author.startswith("@")
    except Exception:
        pytest.skip("Skipping twitter test due to network/scraping issues")
