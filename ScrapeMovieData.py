import bs4
import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pickle
import locale
import pandas as pd
import re
import csv
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
with open('imdb_top_250','rb') as f:
    d = pickle.load(f)
Budget = ''
Runtime=''
Writer = ''
Gross = ''
Genres = ''
##Disclaimer, This script sometimes stops working after a couple of tens requests to IMDB, so instead of saving it to a Pickle file directly i saved the results into a .csv file, if the script stops working just get
##the last ovie number,change it in the range and repeat. Next file is going to merge the dataframe of the top 250 movies with this data.
for i in range(0,250):
    url = 'http://www.imdb.com/title/'+d.iloc[i]['id']+'/'
    print(d.iloc[i]['id'])
    Client = uReq(url)
    Html = Client.read()
    Client.close()
    Soup = soup(Html,'html.parser')
    ##IMDB doesn't always have consistent data so try/except are necessary
    try:
        Writer = Soup.findAll("span",{"class":"itemprop","itemprop":"name"})[1].text
    except:
        Writer = ''
    try:
        Runtime = Soup.findAll('time',{'itemprop':'duration'})[1].text.split(' ')[0]
    except:
        Runtime = '0'
    try:
        genres = ''
        for j in range(len(Soup.findAll('span',{'itemprop':'genre'}))):
            if j != 0:
                genres += '/'
            genres += Soup.findAll('span',{'itemprop':'genre'})[j].text
    except:
        genres = ''
    exists = False
    gross = 0
    budget = 0
    for j in Soup.findAll('h3',{'class':'subheading'}):
        if j.text == 'Box Office':
            exists = True
    if exists:
        for a in Soup.findAll('div',{'class':'txt-block'}):
            if a.h4!= None and a.h4.text == 'Budget:':
                print(a.text)
                try:
                    budget = re.search("£|\$|€",a.text).group(0) + re.sub("\D","",a.text.split('\n')[1])
                except:
                    budget = a.text.split('\n')[1].replace(' ','').replace(',','').split(':')[1].replace('\xa0','')
            if a.h4 != None and a.h4.text == 'Gross:':
                print(a.text)
                try:
                    gross = re.search("£|\$|€",a.text).group(0) + re.sub("\D","",a.text.split('\n')[1])
                except:
                    gross = a.text.split('\n')[1].replace(' ','').replace(',','').split(':')[1].replace('\xa0','')
    with open('films.csv', "a") as output:
         filewriter = csv.writer(output, delimiter=',',quoting=csv.QUOTE_MINIMAL)
         filewriter.writerow([Writer,Runtime,genres,budget,gross])
