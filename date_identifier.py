#import datefinder
#import dateutil.parser as dparser

from datetime import datetime
import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/words_detected/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_0_50.csv')

#get list of all words
words = list(data.loc[:122,'word'])

dates = list()

for s in words:
    s = str (s)
    for fmt in (#all short/long  combinations with dot format
                '%d.%m.%Y', '%d.%m.%y', '%w.%m.%Y', '%w.%m.%y', '%d.%-m.%Y', '%d.%-m.%y','%w.%-m.%Y','%w.%-m.%y', 
                '%Y.%m.%d', '%y.%m.%d', '%Y.%m.%w', '%y.%m.%w', '%Y.%-m.%d', '%y.%-m.%d','%Y.%-m.%w','%y.%-m.%w',
                #all short/long  combinations with hyphen format
                '%d-%m-%Y', '%d-%m-%y', '%w-%m-%Y', '%w-%m-%y', '%d-%-m-%Y', '%d-%-m-%y','%w-%-m-%Y','%w-%-m-%y', 
                '%Y-%m-%d', '%y-%m-%d', '%Y-%m-%w', '%y-%m-%w', '%Y-%-m-%d', '%y-%-m-%d','%Y-%-m-%w','%y-%-m-%w',
                #all short/long  combinations with slash format
                '%d/%m/%Y', '%d/%m/%y', '%w/%m/%Y', '%w/%m/%y', '%d/%-m/%Y', '%d/%-m/%y','%w/%-m/%Y','%w/%-m/%y',
                '%Y/%m/%d', '%y/%m/%d', '%Y/%m/%w', '%y/%m/%w', '%Y/%-m/%d', '%y/%-m/%d','%Y/%-m/%w','%y/%-m/%w',
                #all integer/text combinations 
                '%d. %b %y', '%d %b %y', '%d. %B %y', '%d %B %y', '%w. %b %y', '%w %b %y', '%w. %B %y', '%w %B %y'):
        try:
            date = datetime.strptime(s, fmt).date()
            break
        except ValueError:
            date = 'None'

    dates.append(date)

isDateColumn = pd.DataFrame ({'IsDate' :dates})
data ['IsDate'] = isDateColumn
data.to_csv(datapath + 'data_dates_identified_0_50_.csv', index=False, encoding='utf-8-sig')





'''
#Detects single numbers as Date
for i in words:
    i = str(i)
    try:
        x = dparser.parse(i, dayfirst = True)

    except ValueError:
        x = None

    dates.append(x)

print (dates)
'''

'''
#Returns unclear output
for i in words:
    i = str(i)
    try:
        x = datefinder.find_dates(i)

    except ValueError:
        x = None

    dates.append(x)

print (dates)
'''