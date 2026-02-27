import requests
import xml.etree.ElementTree as ET

def test_reddit_rss():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    url = "https://www.reddit.com/r/technology/.rss"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Reddit RSS Status: {response.status_code}")
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # Reddit RSS is Atom, so namespace is usually needed
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)
            print(f"Found {len(entries)} entries")
            for entry in entries[:5]:
                title = entry.find('atom:title', ns).text
                link = entry.find('atom:link', ns).attrib['href']
                print(f" - {title} ({link})")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"RSS Error: {e}")

test_reddit_rss()
