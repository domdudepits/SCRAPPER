import re
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

url = "https://youtu.be/0pA10Fdr7yM?si=tqjlDYEm9wZKeu3b"

session = HTMLSession()
response = session.get(url)
response = response.html.render()
soup = bs(response.html.raw_html, 'html.parser')
print(soup.find('meta', property="og:title"))