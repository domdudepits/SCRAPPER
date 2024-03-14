from cmath import nan
from datetime import date
import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build
import time as t

song_name = []
label = []
artists = []
album = []


filename = "Combined Sheet_Jio and Wynk.xlsx"
df = pd.read_excel(filename)
urls = df['wynk link']
counter = 0


for url in urls:
 try:
  video_url = url
  session = HTMLSession()
  response = session.get(video_url)
  soup = bs(response.html.html, "html.parser")

  artist = ''
  sname = soup.find('h1', attrs={"class":"heading1"}).text
  song_name.append(sname)
  ar=''
  for a in  soup.find_all('li', attrs={'class': "mt-4"}):
   ar += f"{a.text}, "
  ar = ar[:-2]
  artists.append(ar)
  

  l = soup.find('div', attrs={"class":"text-xs text-wynk-static-black dark:text-wynk-dark-text-secondary leading-6"}).text.split(' • ')
  label.append(l[1])
  
  
  al = soup.find('span', attrs={'class':'text-subtitle-hover cursor-pointer'}).text
  album.append(al)
  
 except:
  print(f"An ERROR occured at this url - {url}")
  song_name.append(None)
  artists.append(None)
  album.append(None)
  label.append(None)
 counter += 1
 print(counter)

 

df['Song Name'] = song_name
df['Album'] = album
df['Label'] = label
df['Artist'] = artists

print(df.head())
df.to_excel(filename, index=False)