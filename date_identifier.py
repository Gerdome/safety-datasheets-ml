#import datefinder
#import dateutil.parser as dparser

from datetime import datetime
import pandas as pd
import numpy as np
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
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv')

data['date_nr'] = np.nan
data['date_type'] = np.nan

#get list of all words
words = list(data.loc[:3000,'word'])

#date_indices= list()

index = -1

for s in words:
    print (index)
    index += 1
    s = str(s)
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
            data.loc[index, 'date_nr'] = date
            
            type = str(data.loc[index-1, 'word']).lower()
            if type.find('datum') != -1:
                data.loc[index, 'date_type'] = type
            else:  
                type =''
                for i in range(3,1): type += str(data.loc[index-i, 'word']).lower()
                data.loc[index, 'date_type'] = type
            break
        except ValueError:
            continue
            

    

# Suche nur auf erster Seite + erstem Wort davor das Datum enthält

#Add to csv
'''isDateColumn = pd.DataFrame ({'IsDate' :dates})
data ['IsDate'] = isDateColumn'''

data.to_csv(datapath + 'data_dates_identified_0_50_.csv', index=False, encoding='utf-8-sig')

print (data.date_type.unique())






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