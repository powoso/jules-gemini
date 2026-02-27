import requests

def test_reddit():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    url = "https://www.reddit.com/r/technology/top.json?limit=5"
    try:
        response = requests.get(url, headers=headers)
        print(f"Reddit Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            for post in data['data']['children']:
                print(f" - {post['data']['title']}")
        else:
            print(response.text[:200])
    except Exception as e:
        print(f"Reddit Error: {e}")

test_reddit()
