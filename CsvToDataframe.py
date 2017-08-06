import bs4
import json
import pandas as pd
import re
import pickle
import csv

columns= ['Writer','Runtime','Genres','Budget','Gross']
d= pd.read_csv('filmsAgain.csv',names= columns)

with open('imdb_top_250','rb') as f:
    b = pickle.load(f)

b['Writer'] = d['Writer']
b['Runtime'] = d['Runtime']
b['Genres'] = d['Genres']
b['Budget'] = d['Budget']
b['Gross_USA'] = d['Gross']
b = b[ ['Title','Lead_Role','Second_Lead','Director','Writer','Runtime','Year','Genres','Budget','Gross_USA','Ratings','Users_Rated','id'] ]
b.head()
with open('ScrapedData3','wb') as D:
    pickle.dump(b,D)

