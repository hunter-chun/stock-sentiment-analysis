from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import requests


#find/incorporate other news sources
tickers = ['ADBE']
newsTables={}
n=20
parsed=[]

for t in tickers:
    url = f"https://www.marketwatch.com/investing/stock/{t}?mod=search_symbol"
    #req = Request(url=url,headers={'user-agent':'my-app/0.0.1'})
    #response = urlopen(req)
    response = requests.get(url)
    headlines = []
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all("h3",{"class":"article__headline"})
    for e in table:
        #cleaning
        s = ' '.join(e.text.split())
        s = s.lower()
        s = re.sub('\[.*?\];:','',s)
        s = re.sub('[\"`\']','',s)
        if s != '':
            headlines.append(s)
    newsTables.update({t:headlines})


vader = SentimentIntensityAnalyzer()
for key in newsTables.keys():
    print(key)
    for h in newsTables[key]:
        print(h)
        score = vader.polarity_scores(h)
        for k in sorted(score):
            print('{0}:{1},'.format(k,score[k]),end='')
        print("\n")
        
        
""" vdf = pd.DataFrame(vals)
scored=scored.join(vdf,rsuffix='_right')
scored['date'] = pd.to_datetime(scored.date).dt.date

means = scored.groupby(['ticker','date']).mean()
means = means.unstack().xs('compound',axis='columns').transpose()

means.plot(kind='bar')
 """