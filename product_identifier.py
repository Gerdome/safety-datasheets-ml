

import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 
#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/labeled/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'chapter_identified.csv', dtype=str)         #basiert auf chapter identified


#get list of all words
words = list(data['word'])



#Einfachster Fall: Name des Produktes ein Wort und findet Produktname
    product_dict = {
        'Handelsname', 'Handelsname:'
    }

l1 = []

for c in product_dict:

    for i, e in enumerate(words):       
        if words[i-1] == c:
             l1.append(i)


# fill in identified labels in data
data['product label'] = '0'
for j in l1:
    data.loc[j,'product label'] = 'produktname'


data.to_csv('product_identified.csv', index=False, encoding='utf-8-sig')


