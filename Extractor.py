import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
from tqdm import tqdm 
import threading

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
            views_data = []
            pdate_data = []
            titles = []
            global trigger
            link = []

            for i, url in enumerate(urls):
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True
                    return views_data, pdate_data, link, titles
                video_url = str(url)
                response = session.get(video_url)
                soup = bs(response.html.html, "html.parser")
                try:
                    views = soup.find("meta", itemprop="interactionCount")['content']
                    pdate = soup.find("meta", itemprop="datePublished")['content']
                    title = soup.find('meta', attrs = {'name' : "title"})['content']

                    titles.append(title)
                    views_data.append(views)
                    pdate_data.append(pdate)
                    link.append(url)
                except:
                    views_data.append('Invalid URL')
                    pdate_data.append('Invalid URL')
                    titles.append('None')
                    link.append(url)
                progress["value"] = (i+1) / len(urls) * 100
                progress.update()
            return views_data, pdate_data, link, titles
            


            


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
        if 'youtube link' in cols:
            urls = df['youtube link']
            views_data = []
            pdate_data = []
            channel_name = []
            title = []
            progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()
            for i, url in enumerate(urls):
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True
                    break
                try:
                    response = session.get(url)
                    soup = bs(response.html.html, "html.parser")
                            
                    # channel_name.append(soup.find("link", itemprop="name")["content"])
                    # title.append(soup.find('meta', property="og:title")["content"])
                    views = soup.find("meta", itemprop="interactionCount")['content']
                    pdate = soup.find("meta", itemprop="datePublished")['content']
                    views_data.append(views)
                    pdate_data.append(pdate)
                except:
                    # channel_name.append('Invalid URL')
                    views_data.append('Invalid URL')
                    pdate_data.append('Invalid URL')
                    # title.append('Invalid URL')
                progress["value"] = (i+1) / len(urls) * 100
                progress.update()
            if not dead or trigger == True:
                views_data.extend(['None']*(len(urls) - len(views_data)))
                pdate_data.extend(['None']*(len(urls) - len(pdate_data)))
                df[f'NEW VIEWS {today}'] = views_data 
                df['DATE'] = pdate_data
                # df['Channle Name'] = channel_name 
                progress.destroy()
                download_button.config(state='active')
                messagebox.showinfo("Data extraction Completed", "You can download the updated file!")
                start_button.config(state='normal')
                stop_button.config(state='disable')
        elif 'savan link' in cols:
            urls = df['savan link']
            plays = []
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
                
                except:
                    labels.append("Invalid URL")
                    plays.append("Invalid URL")
                progress["value"] = (j+1) / len(urls) * 100
                progress.update()
            if not dead or trigger == True:   
                plays.extend(['None']*(len(urls) - len(plays)))
                labels.extend(['None']*(len(urls) - len(labels)))

                df[f"Plays  {today}"] = plays
                df["Labels"] = labels
                progress.destroy()
                download_button.config(state='active')
                messagebox.showinfo("Data extraction Completed", "You can download the updated file!")
                start_button.config(state='normal')
                stop_button.config(state='disable')
        elif 'spotify link' in cols:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            plays, release_dates, artists, labels, titles = [], [], [], [], []
            session = HTMLSession()
            urls = df['spotify link']
            progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
            progress.pack()
            for j, url in enumerate(urls):
                print(j)
                if dead:
                    progress.destroy()
                    download_button.config(state='disable')
                    trigger = True

                    break
                # try:
                driver.get(url)
                response = session.get(url)
                # except:
                #     plays.append('None')
                #     labels.append('None')
                #     release_dates.append('None') 
                #     artists.append('None')
                #     titles.append("None")


                try:
                    play = WebDriverWait(driver,4).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/section/div[1]/div[3]/div[3]/div/span[4]'))
                        ).text 
                    plays.append(play)
                except:
                    plays.append('None')
                try:
                    label = WebDriverWait(driver,4).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/section/div[5]/div/div/p[1]'))
                        ).text
                    labels.append(label)
                except:
                    labels.append('None')
                try:
                    soup = bs(response.html.html, "html.parser")
                    artist = soup.find_all('meta', attrs = {'name' : "music:musician_description"})[0]['content']
                    release_date = soup.find_all('meta', attrs = {'name' : "music:release_date"})[0]['content']
                    title = soup.find('meta', attrs ={'property' : "og:title"})['content'] 
                    
                    release_dates.append(release_date)        
                    artists.append(artist)
                    titles.append(title)
                    
                except:
                    release_dates.append('None')      
                    titles.append("None")
                    artists.append('None')
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
