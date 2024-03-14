from datetime import datetime
from email.policy import default
from flask import Flask, redirect, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession 




def getviews(filename, name):
  df = pd.read_excel(filename)
  urls = df['youtube link']
  views_data = []
  pdate_data = []
  

  for url in urls:
    video_url = url
    session = HTMLSession()
    response = session.get(video_url)
    soup = bs(response.html.html, "html.parser")
    views = soup.find("meta", itemprop="interactionCount")['content']
    pdate = soup.find("meta", itemprop="datePublished")['content']
    views_data.append(views)
    pdate_data.append(pdate)
  df['NEW VIEWS'] = views_data 
  df['NEW DATE'] = pdate_data
  df.to_excel(name, index=False)
  print('done')
  return 0


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
 

@app.route('/', methods=["GET", "POST"])
def home():
  flag = 1
  name = None
  if request.method == "POST":
    name=request.files['file'].filename
    flag=getviews(request.files['file'], name)
  return render_template('index.html', flag=flag, name=name)

if __name__ == '__main__':
 app.run(debug=True, port=8000)