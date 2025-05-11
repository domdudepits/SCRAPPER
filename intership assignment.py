import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build

session = HTMLSession()

response = session.get("https://www.youtube.com/watch?v=pMhkZHl5l7s")
soup = bs(response.html.html, "html.parser")

print(soup.findAll('meta'))
import yt_dlp

urls = [
    "https://www.youtube.com/watch?v=VyK7sMBf4ic",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    # ... add the rest of your 1600 URLs here
]

YDL_OPTIONS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": False,     # We want full metadata
    "skip_download": True,
}

# Create ONE yt-dlp session
with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
    all_data = []
    for url in urls:
        try:
            info = ydl.extract_info(url, download=False)
            all_data.append({
                "title": info.get("title"),
                "views": info.get("view_count"),
                "channel": info.get("channel"),
                "upload_date": info.get("upload_date"),
                "url": url
            })
        except Exception as e:
            all_data.append({
                "error": str(e),
                "url": url
            })

# Now all_data holds your clean metadata
for video in all_data:
    print(video)