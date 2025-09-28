import re
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

url = "https://www.youtube.com/watch?v=VyK7sMBf4ic"

session = HTMLSession()
response = session.get(url)
response = response.html.render()
soup = bs(response.html.raw_html, 'html.parser')
print(soup.find('meta', property="og:title"))



# import yt_dlp

# url = "https://www.youtube.com/watch?v=VyK7sMBf4ic"

# ydl_opts = {}
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)
    
#     title = info.get('title', 'N/A')
#     views = info.get('view_count', 'N/A')
#     likes = info.get('like_count', 'N/A')
#     channel = info.get('uploader', 'N/A')
#     upload_date = info.get('upload_date', 'N/A')  # YYYYMMDD format

#     print(f"Title: {title}")
#     print(f"Channel: {channel}")
#     print(f"Views: {views}")
#     print(f"Likes: {likes}")
#     print(f"Upload Date: {upload_date}")