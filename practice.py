import requests
from bs4 import BeautifulSoup


url = 'https://www.imdb.com/search/title/?release_date=2010-01-01,2014-01-01&num_votes=0,2147483647' 
res = requests.get(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }) 
soup = BeautifulSoup(res.text)
# print(soup)
for i in soup.findAll('li', {'class': "ipc-metadata-list-summary-item"}):
    print(i.find('h3', {'class': "ipc-title__text"}).text[3:])