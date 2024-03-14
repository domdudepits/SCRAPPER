from dataclasses import replace
from requests_html import HTMLSession 
import json
import pandas as pd
import requests
from datetime import date
from bs4 import BeautifulSoup

session = HTMLSession()


# def savan_song_search(list_track):
#   url_format = 'https://www.jiosaavn.com/search/'
#   url_test = url_format + list_track
#   url = url_test.replace(" ", "%20")
#   print(url)
#   response = session.get(url)
#   soup = BeautifulSoup(response.html.html, "html.parser")
#   data = soup.find_all('div', attrs={'class': 'infinite-scroll-component__outerdiv'})
#   print(data)
  
  

# savan_song_search('Baju Band')


# def get_savan_data(url_of_channel):
#   artist_url = url_of_channel
#   token = ''
#   for i in (range(len(artist_url) - 12, len(artist_url))):
#     token += artist_url[i]

#   def get_url(token):
#     urls= []
#     response = requests.get(f"https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}&type=artist&p=0&n_song=50&n_album=50&sub_type=songs&more=true&category=&sort_order=&includeMetaTags=0&ctx=wap6dot0&api_version=4&_format=json&_marker=0")
#     filename = json.loads(response.content)['name']
#     for x in range(0, 100):
#       response = requests.get(f"https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}&type=artist&p={x}&n_song=50&n_album=50&sub_type=songs&more=true&category=&sort_order=&includeMetaTags=0&ctx=wap6dot0&api_version=4&_format=json&_marker=0")
#       data = json.loads(response.content)['topSongs']
#       for i in range(len(data)):
#         urls.append(data[i]['perma_url'])
#     return filename, urls


#   details = {'Song Title': [], 'Plays': [], "Label": []}
#   filename, urls = get_url(token)

#   counter = 0
#   for url in urls:
#     view = []
#     response = session.get(url)
#     soup = BeautifulSoup(response.html.html, "html.parser")
#     views = soup.find('p', attrs={'class' : 'u-centi u-deci@lg u-color-js-gray u-ellipsis@lg u-margin-bottom-tiny@sm'}).text
#     title_song = soup.find('h1', attrs={'class' : 'u-h2 u-margin-bottom-tiny@sm'}).text
#     details['Song Title'].append(title_song)
#     label = soup.find('p', attrs={'class' : 'u-color-js-gray u-ellipsis@lg u-visible@lg'}).text
#     details['Label'].append(label)
#     final_views = ''
#     numbers = [str(x) for x in range(10)]
#     counter += 1
#     print(counter)
#     for i in range(len(views)):
#       view.append(views[i])
#     for i in range(len(view)):
#       if(view[i] == "P"):
#         break
#       if(view[i] in numbers):
#         final_views += view[i]
#     details['Plays'].append(final_views)
  
#   return details, filename


# data, file_name = get_savan_data('https://www.jiosaavn.com/artist/sanam-band-songs/hBK6l30Gz1w_')
# df = pd.DataFrame(data)
# file_name += '.xlsx'
# df.to_excel(file_name, index=False)

def only_plays_and_label(filename):
  df=pd.read_excel(filename)
  urls = df['savan link']
  plays = []
  labels = []
  counter = 0
  for url in urls:
    try:
      view = []
      response = session.get(url)
      soup = BeautifulSoup(response.html.html, "html.parser")
      views = soup.find('p', attrs={'class' : 'u-centi u-deci@lg u-color-js-gray u-ellipsis@lg u-margin-bottom-tiny@sm'}).text
      label = soup.find('p', attrs={'class' : 'u-color-js-gray u-ellipsis@lg u-visible@lg'}).text
      labels.append(label)
      final_views = ''
      numbers = [str(x) for x in range(10)]      
      for i in range(len(views)):
        view.append(views[i])
      for i in range(len(view)):
        if(view[i] == "P"):
          break
        if(view[i] in numbers):
          final_views += view[i]
      plays.append(final_views)
      print(plays)
      
    except:
      print(f"An ERROR occured at this url - {url}")
      labels.append(None)
      plays.append(None)
      
      
      
    counter += 1 
    print(counter)
  df[f"Plays{date.today()}"] = plays
  df["Labels"] = labels
  df.to_excel(filename,index=False)
  print("DONE!!")

only_plays_and_label('jiosaavn.xlsx')