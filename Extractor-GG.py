import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from urllib import request
import pandas as pd
from tqdm import tqdm 
import threading
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from datetime import date
import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from googleapiclient.discovery import build 
from requests_html import HTMLSession
import os
import requests
import yt_dlp
import time

from openpyxl.utils.exceptions import IllegalCharacterError
import re



today = date.today().strftime("%B %d, %Y")

# Create the main window
root = tk.Tk()
root.geometry("500x300") 
root.title("Data Extractor")
file_path = None

upload = ttk.Button(root, text="Upload File", command=lambda:upload_file())
upload.pack(pady=5 )
start_button = ttk.Button(root, text="Start extraction", command=lambda:start_extraction())
stop_button = ttk.Button(root, text="Stop extraction",state='disable', command=lambda:stop_extraction())
label = tk.Label(root, text="")
download_button = ttk.Button(root, text="Download",state='disable', command=lambda:download_file())
label1 = tk.Label(root, text="Extract data of an Entire Channel \n Paste the link of the  YouTube channel below")

link = tk.StringVar()

entry = ttk.Entry(root, textvariable=link)
 





label1.pack(pady=5)
entry.pack()
label.pack(pady=5)
start_button.pack(pady=5)
stop_button.pack(pady=5)
download_button.pack(pady=5)



def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files","*.xlsx")])
    if file_path:
        label.config(text=f"Selected: {file_path}")
        start_button.config(state='active')
def download_file():
    global df,  file_path, dead, channel_name
    if file_path is None:
        filename = channel_name+".xlsx"
    else:
        filename = os.path.basename(file_path)
    # Open a file dialog to select a save location
    filepath = filedialog.asksaveasfilename(initialfile=filename)
    # Save the file to the selected location
    df = clean_illegal_chars(df)
    df.to_excel(f"{filepath}", index=False)
    messagebox.showinfo("Download Complete", "Data has been updated in the parent file " + filename)


def start_extraction():
    
    global dead, trigger
    trigger = False
    dead = False
    start_button.config(state='disable')
    stop_button.config(state='normal')
    # Create a new thread to run the data extraction process
    global extract_thread
    extract_thread = threading.Thread(target=only_views, daemon=True)
    extract_thread.start()
    

def stop_extraction():
    global dead, extract_thread
    ans = messagebox.askquestion("Interupted", "You really want to stop?")
    if( ans == 'yes'):
        dead = True
        entry.delete(0, tk.END)
        
    start_button.config(state='normal')
    stop_button.config(state='disable')


def clean_illegal_chars(df):
    import re
    # Go column by column
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[\x00-\x1F\x7F-\x9F]', '', x))
    return df


def only_views():
    global dead, df, link, channel_name, trigger
    session = HTMLSession()
    if link.get() != '':
        channel_url = link.get()
        api_key = 'AIzaSyA6l6-3Hl3X3pCgXS-2te5BQoVbWHjgIYA'
        youtube = build('youtube', 'v3', developerKey = api_key)
        progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        progress.pack()


        def get_channel_videos(channel_id):
            res = youtube.channels().list(id = channel_id, part = 'contentDetails').execute()
            playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            videos = []
            next_page_token = None
            while 1:
                res1 = youtube.playlistItems().list(playlistId = playlist_id, part = 'snippet', maxResults = 50, pageToken = next_page_token).execute()
                videos += res1['items']
                channel_name = res1['items'][0]['snippet']['channelTitle']
                next_page_token = res1.get('nextPageToken')
                if next_page_token is None:
                    break
            return videos, channel_name



        def make_url(video_id):
            for id in video_id:
                url = 'https://www.youtube.com/watch?v='
                url += id
                urls.append(url)
            return urls

        def get_data(urls):
            views = []
            date = []
            title = []
            global trigger
            link = []

            session = requests.Session()

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }

            session.headers.update(headers)


            for i, url in enumerate(urls):
                if i % 50 == 0:
                    time.sleep(1)
                
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True
                    return views, date, link, title
                
                video_url = str(url)
                
                try:
                    time.sleep(0.2)
                    r = session.get(video_url, timeout=10)
                    
                    html = r.text
                    
                    json_text = re.search(
                        r"ytInitialPlayerResponse\s*=\s*(\{.+?\});",
                        html
                    ).group(1)
                    
                    data = json.loads(json_text)
                except:
                    views = None
                    title = None
                    date = None
                
                try:
                    video_details = data["videoDetails"]
                    views.append(video_details["viewCount"])
                    title.append(video_details["title"])
                    link.append(url)
                    
                    date.append(data["microformat"]["playerMicroformatRenderer"]["uploadDate"][:10])

                except Exception:
                    views.append("None")
                    title.append("None")
                    date.append("None")
                    link.append(url)
                    
                progress["value"] = (i+1) / len(urls) * 100
                progress.update()
            return views, date, link, title
            


            


        response = session.get(channel_url)
        soup = bs(response.html.html, "html.parser")
        id = soup.find('meta', property="al:ios:url")["content"]
        id_indx = id.rfind('/')
        channel_id = id[id_indx+1:]

        videos, channel_name= get_channel_videos(channel_id)
        title, urls, video_id = [], [], []
        for video in videos:
            video_id.append(video['snippet']['resourceId']['videoId'])


        urls = make_url(video_id)
        views, pdate, link, title = get_data(urls)
        if not dead or trigger == True:
            channel_details = {'youtube link': [],'TITLE': [], 'VIEWS': [], 'DATE': []}
            channel_details['TITLE'] = title
            channel_details['DATE'] = pdate
            channel_details['VIEWS'] = views
            channel_details['youtube link'] = link
            df = pd.DataFrame(channel_details)
            progress.destroy()
            download_button.config(state='active')
            messagebox.showinfo("Data extraction Completed", "You can download the updated file!")
            start_button.config(state='normal')
            stop_button.config(state='disable')

    
    else: 
        df = pd.read_excel(file_path)
        cols = df.columns
        start_idx = 0
        
        
        
        if start_idx == 0:
            start_idx = 2
        if 'youtube link' in cols:
            col_views = f"NEW VIEWS {today}"

            # Ensure columns exist
            for col in [col_views, "TITLE", "DATE", "Channel Name"]:
                if col not in df.columns:
                    df[col] = None
            df["DATE"] = df["DATE"].astype("string")
            df["TITLE"] = df["TITLE"].astype("string")
            df[col_views] = df[col_views].astype("string")
            df["Channel Name"] = df["Channel Name"].astype("string")
            
            progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()

            urls = df.loc[start_idx-2: , "youtube link"].tolist()

            session = requests.Session()

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }

            session.headers.update(headers)
            for i, url in enumerate(urls):
                if i % 50 == 0:
                    time.sleep(1)
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True
                    break
                
                try:
                    time.sleep(0.2)
                    r = session.get(url, timeout=10)
                    
                    html = r.text
                    
                    json_text = re.search(
                        r"ytInitialPlayerResponse\s*=\s*(\{.+?\});",
                        html
                    ).group(1)
                    
                    data = json.loads(json_text)
                except:
                    print(f"Error at url ----> {url}")
                    views = None
                    title = None
                    channel = None
                    date = None
                row = (start_idx-2) + i
                
                try:
                    video_details = data["videoDetails"]
                    views = video_details["viewCount"]
                    title = video_details["title"]
                    
                    channel = video_details["author"]
                    date = data["microformat"]["playerMicroformatRenderer"]["uploadDate"][:10]

                except Exception:
                    views = None
                    title = None
                    channel = None
                    date = None

                # Write directly to dataframe
                df.loc[row, col_views] = views
                df.loc[row, "TITLE"] = title
                df.loc[row, "Channel Name"] = channel
                df.loc[row, "DATE"] = date

                # Update progress bar
                progress["value"] = (i+1) / len(urls) * 100
                progress.update()
                
                print(f"{start_idx + i} / {views} / {title}")
                    

            if not dead or trigger == True:
                # # views_data.extend(['None']*(len(urls) - len(views_data)))
                # # pdate_data.extend(['None']*(len(urls) - len(pdate_data)))
                # # titles.extend(['None']*(len(urls) - len(pdate_data)))
                # # channel_name.extend(['None']*(len(urls) - len(pdate_data)))
                # end_idx = start_idx + len(views_data)

                # df.loc[start_idx:end_idx-1, f'NEW VIEWS {today}'] = views_data
                # df.loc[start_idx:end_idx-1, 'DATE'] = pdate_data
                # df.loc[start_idx:end_idx-1, 'TITLE'] = titles
                # df.loc[start_idx:end_idx-1, 'Channel Name'] = channel_name
                progress.destroy()
                download_button.config(state='active')
                messagebox.showinfo("Data extraction Completed", "You can download the updated file!")
                start_button.config(state='normal')
                stop_button.config(state='disable')
        if 'savan link' in cols:
            urls = df['savan link']
            plays, titles, artists = [], [], []
            labels = []
            progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()
            for j, url in enumerate(urls):
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True
                    break
                try:
                    view = []
                    response = session.get(url)
                    soup = bs(response.html.html, "html.parser")
                    views = soup.find('p', attrs={'class' : 'u-centi u-deci@lg u-color-js-gray u-ellipsis@lg u-margin-bottom-tiny@sm'}).text
                    label = soup.find('p', attrs={'class' : 'u-color-js-gray u-ellipsis@lg u-visible@lg'}).text
                    title = soup.find('h1', attrs={'class' : 'u-h2 u-margin-bottom-tiny@sm'}).text
                    try:
                        artist = soup.find('p', attrs={'class' : 'u-color-js-gray u-ellipsis@lg u-margin-bottom-tiny@sm'}).find_all('a')[1].text
                    except Exception as e:
                        print(f"error while extracting artist name at URL -> {url}")
                    labels.append(label)
                    titles.append(title)
                    artists.append(artist)
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
                
                except Exception as e:
                    print(e)
                    labels.append("Invalid URL")
                    plays.append("Invalid URL")
                    titles.append("Invalid URL")
                    artists.append("Invalid URL")

                progress["value"] = (j+1) / len(urls) * 100
                progress.update()
            if not dead or trigger == True:   
                plays.extend(['None']*(len(urls) - len(plays)))
                labels.extend(['None']*(len(urls) - len(labels)))

                df[f"Plays  {today}"] = plays
                df["Labels"] = labels
                df['Title'] = titles
                df['Artists'] = artists
                progress.destroy()
                download_button.config(state='active')
                messagebox.showinfo("Data extraction Completed", "You can download the updated file!")
                start_button.config(state='normal')
                stop_button.config(state='disable')
        if 'spotify link' in cols:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            plays, release_dates, artists, labels, titles = [], [], [], [], []
            session = HTMLSession()
            urls = df['spotify link']
            progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()
            for j, url in enumerate(urls):
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True

                    break
                try:
                    driver.get(url)
                    response = session.get(url)
                    page = driver.page_source
                    soup = bs(page, 'html.parser')
                    try:
                        play = WebDriverWait(driver,5).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@data-testid='playcount']"))
                            ).text
                        print(play)
                        plays.append(play)
                    except:
                        plays.append('None')
                        print(f"Error while extracting plays in url -> {url}")
                    try:
                        label = WebDriverWait(driver,5).until(
                            EC.presence_of_element_located((By.XPATH , '//*[@id="main-view"]/div/div[2]/div[1]/div/main/section/div[4]/div/div/p[1]'))
                            ).text
                        labels.append(label)

                    except:
                        labels.append('None')
                        print(f"Error while extracting label in url -> {url}")

                    try:
                        soup = bs(response.html.html, "html.parser")
                        artist = WebDriverWait(driver,5).until(
                            EC.presence_of_element_located((By.XPATH , '//div[@class="FYDVy8qxy_QugEOZ P2bsavgZEZcO4YZh"]'))
                            ).text
                        print(artist)
                        artists.append(artist)
                    except Exception as e:
                        artists.append('None')
                        print("error while getting artist name")
                        
                        
                    try:
                        release_date = WebDriverWait(driver,5).until(
                            EC.presence_of_element_located((By.XPATH , '//*[@id="main-view"]/div/div[2]/div[1]/div/main/section/div[4]/div/p'))
                            ).text
                        release_dates.append(release_date)        
                        
                    except Exception as e:
                        release_dates.append('None')  
                        print("error while getting Release Date")    
                        
                        
                    try:
                        title = WebDriverWait(driver,5).until(
                            EC.presence_of_element_located((By.XPATH , '//*[@id="main-view"]/div/div[2]/div[1]/div/main/section/div[1]/div[2]/div[3]/span[2]/span/h1'))
                            ).text
                        titles.append(title)
                    except Exception as e:
                        titles.append("None")
                        print("error while getting Title")

                except:
                    print(f"Error while fetching the URL -> {url}")
                    plays.append('None')
                    labels.append('None')
                    release_dates.append('None') 
                    artists.append('None')
                    titles.append("None")


                

                progress["value"] = (j+1) / len(urls) * 100
                progress.update()
            if not dead or trigger == True:
                if trigger == True:
                    plays.extend(['None']*(len(urls) - len(plays)))
                    release_dates.extend(['None']*(len(urls) - len(release_dates)))
                    artists.extend(['None']*(len(urls) - len(artists)))
                    labels.extend(['None']*(len(urls) - len(labels)))
                    titles.extend(['None']*(len(urls) - len(titles)))

                df[f'NEW PLAYS {today}'] = plays 
                df['DATE'] = release_dates
                df['ARTISTS'] = artists
                df['LABELS'] = labels
                df['TITLE'] = titles
                progress.destroy()
                download_button.config(state='active')
                messagebox.showinfo("Data extraction Completed", "You can download the updated file!")
                start_button.config(state='normal')
                stop_button.config(state='disable')



        else:
            messagebox.showwarning('WARNING!', 'The Chosen file does not contain the relevent URLs \n          OR \n The names of the columns containg URLs did not match')
            start_button.config(state='disable')
            stop_button.config(state='disable')

   
root.mainloop()