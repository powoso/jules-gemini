import requests

def debug_nitter_response():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    url = "https://nitter.aosus.link/elonmusk/rss"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print("Content start:")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

debug_nitter_response()
