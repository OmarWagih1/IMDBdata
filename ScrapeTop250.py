import bs4
import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pickle

url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'

Client = uReq(url)

Html = Client.read()

Client.close()

Soup = soup(Html,"html.parser")

Titles = Soup.findAll("td",{"class":"titleColumn"})
Ratings = Soup.findAll("td",{"class":"imdbRating"})

index = ["Title","id","Ratings","Users_Rated","Director","Lead_Role","Second_Lead","Year"]
titleArray = []
idArray = []
directorArray = []
firstStar = []
ratingArray = []
usersArray = []
secondStar = []
yearArray = []
Dataframe = pd.DataFrame(columns = index)
for i in Ratings:
    ratingArray.append(float(i.strong.text))
    x = 0
    length = len(i.strong['title'].split(' ')[3].split(','))
    for j in range(length):
            x += int(i.strong['title'].split(' ')[3].split(',')[j])*(10**(length-j-1))**3
    usersArray.append(x)
    x = 0
for i in Titles:
    titleArray.append(i.a.text)
    idArray.append(i.a['href'].split('/')[2])
    directorArray.append(i.a['title'].split(',')[0].split('(')[0])
    firstStar.append(i.a['title'].split(',')[1])
    secondStar.append(i.a['title'].split(',')[2])
    yearArray.append(int(i.span.text.split('(')[1][0:4]))

Dataframe['Title'] = titleArray
Dataframe['id'] = idArray
Dataframe['Director'] = directorArray
Dataframe['Ratings'] = ratingArray
Dataframe['Users_Rated'] = usersArray
Dataframe['Lead_Role'] = firstStar
Dataframe['Second_Lead'] = secondStar
Dataframe['Year'] = yearArray
with open('imdb_top_250','wb') as f:
  pickle.dump(Dataframe,f)
print(Dataframe.head())

    
