import requests

def test_reddit_3():
    headers = {
        'User-Agent': 'MyScraperApp/1.0'
    }
    url = "https://www.reddit.com/r/technology/top.json?limit=5"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Reddit Status: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            data = response.json()
            for post in data['data']['children']:
                print(f" - {post['data']['title']}")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

test_reddit_3()
