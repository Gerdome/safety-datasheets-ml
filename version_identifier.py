import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os
import re

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv', dtype=str , index_col = 0)

#get list of all words
words = list(data['word'])

version_dict = {
    'Versionsnummer', 'Version', 'Versionsnummer:' , 'Version:' , 'Revisions-Nr:' , 'Revisions-Nr',
    'Revisions-nr' , 'Revisionsnummer' , 'Revisionsnummer:', 'Rev-Nr.:' , 'Rev-Nr:' , 'Version-Nr'
}

l1 = []

for c in version_dict:

    for i, e in enumerate(words):       
        if words[i-1] == c:
            if words[i] == '(': # Versionsnummer und in Klammern alte Versionsnummer
                 l1.append(i+4)
            elif words[i] == ':': # wenn zwischen Version und : Leerzeichen vorkommmt -> naechstes 
                 if words[i-4]== 'Überarbeitet':
                    l1.append(i+3)
                 elif words[i-5] != 'Ersetzt' and words[i-3] != 'Ersetzt':
                    l1.append(i+1)
            elif words[i] == '.': 
                   l1.append(i+2)
            else:
                 l1.append(i)
            


# fill in identified labels in data
data['version label'] = '0'
for j in l1:
    data.loc[j,'version label'] = 'version'

data.to_csv('version_identified.csv', encoding='utf-8-sig')
