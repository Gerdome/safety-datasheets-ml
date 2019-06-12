


#library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
import pandas as pd
#The Natural Language Toolkit (NLTK) is an open source Python library for Natural Language Processing
#Formally, a conditional frequency distribution can be defined as a function that maps from each condition to the FreqDist for the experiment under that condition.
from nltk import FreqDist
#https://pypi.org/project/stop-words/#basic-usage
#https://www.nltk.org/api/nltk.corpus.html
from nltk.corpus import stopwords
#The main purpose of the OS module is to interact with your operating system. The primary use I find for it is to create folders, remove folders, move folders, and sometimes change the working directory.
import os 

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/labeled/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'chapter_identified.csv', dtype=str)


#get list of all words
words = list(data['word'])

#get list of all words from index 0 until 100000 (first 4 pdfs)
#words = list(data.loc[:10000, 'word'])


#define dictionary (vgl. https://docs.google.com/document/d/1a4kwA13XB8EXB1CHJ8fBRW24CaJZvohraroD2Dyn204/edit#)

'''
#Problem 1
verordnung_dict1 = {
    'Verordnung (EU) Nr.', 'Verordnung (EU)', 'Verordnung (EG) Nr.', 'Verordnung (EG)'
}

l1 = []

for c in verordnung_dict1:
#https://stackoverflow.com/questions/22171558/what-does-enumerate-mean/22171593  enumarate
    for i, e in enumerate(words):       
        if words[i-1] == c:
             l1.append(i)

'''

'''
#Problem 2
verordnung_dict2 = {
    '(REACH)'
}

l2 = []
#i+1
for c in verordnung_dict2:
    for i, e in enumerate(words):       
        if words[i-1] == c:
             l2.append(i)

# fill in identified labels in data
data['verordnung label'] = '0'
for j in l2:
    data.loc[j,'verordnung label'] = 'verordnung'


data.to_csv('directive_identified.csv', index=False, encoding='utf-8-sig')
'''



#Problem 3
verordnung_dict3 = {
    'EU-Verordnung'
}

l3 = []

for c in verordnung_dict3:
#https://stackoverflow.com/questions/22171558/what-does-enumerate-mean/22171593  enumarate
    for i, e in enumerate(words):       
        if words[i-1] == c:
             l3.append(i)





# fill in identified labels in data
data['verordnung label'] = '0'
for j in l3:
    data.loc[j,'verordnung label'] = 'verordnung'


data.to_csv('directive_identified.csv', index=False, encoding='utf-8-sig')




#Merge lists