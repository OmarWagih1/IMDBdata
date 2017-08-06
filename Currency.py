import pandas as pd
import requests
import numpy as np
import pickle
import json
import requests, re
##This is not accurate, some of these movies were produced 50+ years ago in which the currency value may have changed significantly.
with open('ScrapedData3','rb') as f:
  d = pickle.load(f)
Currencies = requests.get('http://api.fixer.io/latest?base=USD').json()
Budgets = []
pd.set_option('display.float_format', lambda x: '%.1f' % x)
for i in range(0,250):
    Budget = d.iloc[i]['Budget']
    print(Budget)
    print( float(re.search(r'\d+', Budget).group()))
    if Budget.startswith('€'):
        Budgets.append(int(re.search(r'\d+', Budget).group())/Currencies['rates']['EUR'])
    elif Budget.startswith('INR'):
        Budgets.append(int(re.search(r'\d+', Budget).group())/Currencies['rates']['INR'])
    elif Budget.startswith('JPY'):
        Budgets.append(int(re.search(r'\d+', Budget).group())/Currencies['rates']['JPY'])
    elif Budget.startswith('INR'):
        Budgets.append(int(re.search(r'\d+', Budget).group())/Currencies['rates']['INR'])
    elif Budget.startswith('£'):
        Budgets.append(int(re.search(r'\d+', Budget).group())/Currencies['rates']['GBP'])
    elif Budget.startswith('$'):
        Budgets.append(int(re.search(r'\d+', Budget).group()))
    else:
        Budgets.append(np.nan)

d['Budget'] = Budgets
d['Gross_USA']=d['Gross_USA'].replace('0',np.nan)
d['Gross_USA'] = d['Gross_USA'].str.replace(r'\D+', '').astype(float)

with open('NumberReady','wb') as f:
    pickle.dump(d,f)
print(d.head(100))
