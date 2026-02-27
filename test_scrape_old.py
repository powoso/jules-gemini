import requests

def test_old_reddit():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = "https://old.reddit.com/r/technology/top.json?limit=5"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Old Reddit Status: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

test_old_reddit()
