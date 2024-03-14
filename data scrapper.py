from datetime import datetime
import pandas as pd
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from googleapiclient.discovery import build

data = {"Txn Hash": [],
        "Method": [],
        "block": [],
        "Age": [],
        "From": [],
        "To":[],
        "Value": [],
        "Txn Fee":[]}


for i in range(1, 20):
 video_url = f"https://bscscan.com/txs?p={i}"
 session = HTMLSession()
 response = session.get(video_url)
 soup = bs(response.html.html, "html.parser")
 table = soup.find('table', class_='table table-hover')
 for row in table.tbody.find_all('tr'):
  # Find all data for each column
  columns = row.find_all('td')
  txn_hash = columns[1].text#TXN HASH
  method = columns[2].span.get('title')#METHOD
  block = columns[3].text #BLOCK
  age = columns[4].span.get('title') #AGE
  frm = columns[6].text #FROM
  to = columns[8].a.text #TO
  value = columns[9].text #VALUE
  txn_fee = columns[10].text #TXN FEE
  data["Txn Hash"].append(txn_hash)
  data["Age"].append(age)
  data["block"].append(block)
  data["From"].append(frm)
  data["Method"].append(method)
  data["To"].append(to)
  data["Txn Fee"].append(txn_fee)
  data["Value"].append(value)
  df = pd.DataFrame(data)
 print(f"page {i} done scrapping")


print(df.shape)


filename = f"transaction details.xlsx"
df.to_excel(filename, index=False)