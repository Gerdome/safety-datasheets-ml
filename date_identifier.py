import datefinder
import dateutil.parser as dparser
import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 


#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/objects_detected/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'full_data_0_50.csv')

#get list of all words
words = list(data.loc[:122, 'Content'])

dates = list ()

'''
for i in words:
    i = str(i)
    try:
        x = dparser.parse(i)

    except ValueError:
        x = None

    dates.append(x)

print (dates)

'''
for i in words:
    i = str(i)
    try:
        x = datefinder.find_dates(i)

    except ValueError:
        x = None

    dates.append(x)

print (dates)
