import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build


session = HTMLSession()
response = session.get("https://www.youtube.com/@PMCSANTSANDESH/videos")
soup = bs(response.html.html, "html.parser")
 
for i in soup.findAll('meta'):
    print(i)