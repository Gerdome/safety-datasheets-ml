import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv', dtype=str)

#get list of all words
words = list(data['word'])

subchapter_dict = {}

subschapter = ( '1.1','1.2','1.3','1.4',
                '2.1','2.2','2.3',
                '3.1','3.2',
                '4.1','4.2','4.3',
                '5.1','5.2','5.3',
                '6.1','6.2','6.3','6.4',
                '7.1','7.2','7.3',
                '8.1','8.2',
                '9.1','9.2',
                '10.1','10.2','10.3','10.4','10.5','10.6',
                '11.1',
                '12.1','12.2','12.3','12.4','12.5','12.6',
                '13.1',
                '14.1','14.2','14.3','14.4','14.5','14.6','14.7','14.8',
                '15.1','15.2',
                '16'
                )

for c in subschapter:
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == c:
             l1.append(i)
    subchapter_dict[c] = l1


# fill in identified labels in data
data['subchapter label'] = '0'
for c in subschapter:
    for j in subchapter_dict[c]:
        data.loc[j,'subchapter label'] = 'Header Subchapter ' + c

data.to_csv('subchapter_identified.csv', index=False, encoding='utf-8-sig')

