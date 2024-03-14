import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build


session = HTMLSession()
response = session.get("https://mail.google.com/mail/u/0/#inbox")
soup = bs(response.html.html, "html.parser")

for i in soup.find_all("input", {"type": "email"}):
 print(i)