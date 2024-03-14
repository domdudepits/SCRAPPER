from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build 

df = pd.read_excel('open.xlsx')
links = df['spotify link']

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
plays, release_dates, artists = [], [], []
session = HTMLSession()
count = 1


for link in links:
    driver.get(link)
    response = session.get(link)
    print(count)

    try:
        
        play = WebDriverWait(driver,3).until(
               EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[1]/div[5]/div/span[4]'))
            ).text 
        label = WebDriverWait(driver,3).until(
               EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[5]/div/div/p[1]'))
            ).text
        
        soup = bs(response.html.html, "html.parser")
        artist = soup.find_all('meta', attrs = {'name' : "music:musician_description"})[0]['content']
        release_date = soup.find_all('meta', attrs = {'name' : "music:release_date"})[0]['content'] 
        plays.append(play)
        release_dates.append(release_date)        
        artists.append(artist)
        
    except:
        plays.append('None')
        release_dates.append('None')        
        artists.append('None')
    count += 1
print(len(plays), len(artists), len(release_dates))
# df['Plays'] = plays
# df['Release Dates'] = release_dates
# df['Artists'] = artists
# df.to_excel('open.xlsx')
driver.quit()