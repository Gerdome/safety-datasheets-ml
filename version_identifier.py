import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/words_detected_ordered/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv', dtype=str)

#get list of all words
words = list(data['word'])

version_dict = {
    'Versionsnummer', 'Version', 'Versionsnummer:' , 'Version:' , 'Revisions-Nr:' , 'Revisions-Nr',
    'Revisions-nr' , 'Revisionsnummer' , 'Revisionsnummer:', 'Rev-Nr.:' , 'Rev-Nr:'
}

l1 = []

for c in version_dict:

    for i, e in enumerate(words):       
        if words[i-1] == c:
             l1.append(i)


# fill in identified labels in data
data['version label'] = '0'
for j in l1:
    data.loc[j,'version label'] = 'version'

data.to_csv('version_identified.csv', index=False, encoding='utf-8-sig')
