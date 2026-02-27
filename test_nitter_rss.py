import requests
import xml.etree.ElementTree as ET

def test_nitter_rss():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    # Trying a few known instances
    instances = [
        "https://nitter.net",
        "https://nitter.cz",
        "https://nitter.poast.org",
        "https://nitter.privacydev.net"
    ]

    for instance in instances:
        url = f"{instance}/elonmusk/rss"
        print(f"Testing {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("Success!")
                try:
                    root = ET.fromstring(response.content)
                    items = root.findall('channel/item')
                    print(f"Found {len(items)} items")
                    for item in items[:3]:
                        title = item.find('title').text
                        print(f" - {title[:50]}...")
                    break
                except Exception as e:
                    print(f"Parsing error: {e}")
            else:
                print("Failed.")
        except Exception as e:
            print(f"Error: {e}")

test_nitter_rss()
