import pandas as pd

df = pd.read_excel("Book1 (1).xlsx")
urls = []
start = 283
print(df.loc[start - 2, 'TITLE'])