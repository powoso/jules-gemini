from ntscraper import Nitter

def test_ntscraper():
    scraper = Nitter(log_level=1, skip_instance_check=False)
    try:
        tweets = scraper.get_tweets("elonmusk", mode='user', number=5)
        print(f"Found {len(tweets['tweets'])} tweets")
        for tweet in tweets['tweets']:
            print(f" - {tweet['text'][:50]}...")
    except Exception as e:
        print(f"Error: {e}")

test_ntscraper()
