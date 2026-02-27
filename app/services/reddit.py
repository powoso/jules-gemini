import requests
import xml.etree.ElementTree as ET
from app.models import SocialMediaPost
from datetime import datetime
import re

def scrape_subreddit(subreddit: str = "technology", limit: int = 10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    url = f"https://www.reddit.com/r/{subreddit}/.rss?limit={limit}"

    posts = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # Reddit RSS is Atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)

            for entry in entries:
                try:
                    title = entry.find('atom:title', ns).text
                    link = entry.find('atom:link', ns).attrib['href']
                    updated = entry.find('atom:updated', ns).text
                    author_elem = entry.find('atom:author', ns)
                    author_name = author_elem.find('atom:name', ns).text if author_elem is not None else "Unknown"
                    content_html = entry.find('atom:content', ns).text if entry.find('atom:content', ns) is not None else ""

                    # Extract image if available (basic check)
                    media_url = None
                    if content_html:
                        img_match = re.search(r'<img src="([^"]+)"', content_html)
                        if img_match:
                            media_url = img_match.group(1)

                    # Create ID from link
                    post_id = link.split('/')[-2] if link.endswith('/') else link.split('/')[-1]

                    posts.append(SocialMediaPost(
                        id=post_id,
                        source="reddit",
                        author=f"u/{author_name.replace('/u/', '')}",
                        content=title,
                        url=link,
                        timestamp=updated,
                        media_url=media_url,
                        avatar_url="https://www.redditstatic.com/avatars/defaults/v2/avatar_default_1.png" # Placeholder
                    ))
                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue
        else:
            print(f"Reddit RSS fetch failed: {response.status_code}")
    except Exception as e:
        print(f"Reddit scraper error: {e}")

    return posts
