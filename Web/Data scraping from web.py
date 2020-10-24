import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
print(type(soup))
title = soup.title
print(title)
text = soup.get_text()
print(soup.text)
soup.find_all('a')
all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))
rows = soup.find_all('tr')
print(rows[:10])
for row in rows:
    row_td = row.find_all('td')
    print(row_td)
    print(type(row_td))
    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    print(cleantext)
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '', str_cells))
    list_rows.append(clean2)
    print(clean2)
    print(type(clean2))
df = pd.DataFrame(list_rows)
print(df.head(10))
df1 = df[0].str.split(',', expand=True)
print(df1.head(10))
df1[0] = df1[0].str.strip('[')
print(df1.head(10))
col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)
df2 = pd.DataFrame(all_header)
print(df2.head())
df3 = df2[0].str.split(',', expand=True)
print(df3.head())
frames = [df3, df1]
df4 = pd.concat(frames)
print(df4.head(10))
df5 = df4.rename(columns=df4.iloc[0])
print(df5.head())
print(df5.info())
print(df5.shape)
df6 = df5.dropna(axis=0, how='any')
df7 = df6.drop(df6.index[0])
print(df7.head())
df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)
print(df7.head())
df7['Team'] = df7['Team'].str.strip(']')
print(df7.head())
