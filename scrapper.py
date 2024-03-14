from datetime import date
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build 
from tqdm import tqdm
# import pafy
# import youtube_dl

# api_key2 = "AIzaSyBy0hx5r2bcvEfdAy3rLi4OXzornce6UDY"


def only_views(filename):
  df = pd.read_excel(filename)
  urls = df['youtube link']
  views_data = []
  pdate_data = []
  channel_name = []
  title = []
  

  for url in tqdm(urls):
    try:
      video_url = url
      session = HTMLSession()
      response = session.get(video_url)
      soup = bs(response.html.html, "html.parser")
       
      # channel_name.append(soup.find("link", itemprop="name")["content"])
      # title.append(soup.find('meta', property="og:title")["content"])
      views = soup.find("meta", itemprop="interactionCount")['content']
      pdate = soup.find("meta", itemprop="datePublished")['content']
      views_data.append(views)
      pdate_data.append(pdate)
    except Exception as e:
      # df.drop(counter)
      # channel_name.append(None)
      views_data.append('Invalid URL')
      pdate_data.append('Invalid URL')
      # title.append(None)
      # print(e.args)
    
    # like = vid.likes
    
    # likes.append(like)
    # counter += 1
  df[f'NEW VIEWS {date.today().strftime("%B %d, %Y")}'] = views_data 
  df['DATE'] = pdate_data
  # df['Channle Name'] = channel_name 
  print(df.head())
  df.to_excel(filename, index=False)
 
only_views('youtube data.xlsx')

# def youtube_data_extracter(channel_url):
#   api_key = 'AIzaSyA6l6-3Hl3X3pCgXS-2te5BQoVbWHjgIYA'
#   youtube = build('youtube', 'v3', developerKey = api_key)


#   def get_channel_videos(channel_id):
#     res = youtube.channels().list(id = channel_id, part = 'contentDetails').execute()
#     playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#     videos = []
#     next_page_token = None
#     channel_name = None
#     while 1:
#       res1 = youtube.playlistItems().list(playlistId = playlist_id, part = 'snippet', maxResults = 50, pageToken = next_page_token).execute()
#       channel_name = res1['items'][0]['snippet']['channelTitle']
#       videos += res1['items']
#       next_page_token = res1.get('nextPageToken')
#       if next_page_token is None:
#         break
#     return videos, channel_name



#   def make_url(video_id):
#     for id in video_id:
#       url = 'https://www.youtube.com/watch?v='
#       url += id
#       urls.append(url)
#     return urls

#   def get_data(urls):
#     views_data = []
#     pdate_data = []
#     link = []
#     for url in tqdm(urls):
#       video_url = str(url)
#       session = HTMLSession()
#       response = session.get(video_url)
#       soup = bs(response.html.html, "html.parser")
#       try:
#         views = soup.find("meta", itemprop="interactionCount")['content']
#         pdate = soup.find("meta", itemprop="datePublished")['content']
#         views_data.append(views)
#         pdate_data.append(pdate)
#         link.append(url)
#       except:
#         views_data.append('Invalid URL')
#         pdate_data.append('Invalid URL')
#         link.append(url)
      
#     return views_data, pdate_data, link
      


#   def making_Excel_file(title, pdate, views, link, filename):
#     channel_details = {'youtube link': [],'TITLE': [], 'VIEWS': [], 'DATE': []}
#     channel_details['TITLE'] = title
#     channel_details['DATE'] = pdate
#     channel_details['VIEWS'] = views
#     channel_details['youtube link'] = link
#     df = pd.DataFrame(channel_details)
#     df.to_excel(filename, index=False)


#   session = HTMLSession()
#   response = session.get(channel_url)
#   soup = bs(response.html.html, "html.parser")
#   channel_id = soup.find('meta', itemprop='channelId')['content']

#   videos, channel_name = get_channel_videos(channel_id)
#   title, date, urls, video_id = [], [], [], []
#   filename = channel_name + '.xlsx'
#   for video in videos:
#     title.append(video['snippet']['title'])
#     video_id.append(video['snippet']['resourceId']['videoId'])
#     date.append(video['snippet']['publishedAt'])


#   urls = make_url(video_id)
#   views, pdate, link = get_data(urls)
#   making_Excel_file(title, pdate, views, link, filename)

# youtube_data_extracter('https://www.youtube.com/@rajshrisoul/videos')