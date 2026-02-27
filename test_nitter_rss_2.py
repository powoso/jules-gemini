import requests
import xml.etree.ElementTree as ET

def test_nitter_rss_2():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    # Instances from the gist
    instances = [
        "https://twitt.re",
        "https://nitter.dashy.a3x.dn.nyx.im",
        "https://nitter.privacydev.net",
        "https://xcancel.com",
        "https://nitter.poast.org",
        "https://nitter.pek.li",
        "https://nitter.aishiteiru.moe",
        "https://nitter.aosus.link",
        "https://nitter.10qt.net"
    ]

    for instance in instances:
        url = f"{instance}/elonmusk/rss"
        print(f"Testing {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("Success!")
                try:
                    root = ET.fromstring(response.content)
                    items = root.findall('channel/item')
                    print(f"Found {len(items)} items")
                    for item in items[:1]:
                        title = item.find('title').text
                        print(f" - {title[:50]}...")
                    # If we find a working one, we can stop for now or keep checking to see reliability
                    break
                except Exception as e:
                    print(f"Parsing error: {e}")
            else:
                print("Failed.")
        except Exception as e:
            print(f"Error: {e}")

test_nitter_rss_2()
