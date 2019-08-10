from datetime import datetime
import pandas as pd
import numpy as np
from nltk import FreqDist
from nltk.corpus import stopwords
import os 
import re
from operator import itemgetter

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_all_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Labels
date_labels = {
    #1. Druckdatum/Erstellung
    'Druck':  ['druck', 'ausgabe', 'ausstellung', 'erstellung', 'sd-datum', 'erstellt', 'ausgestellt'],
    #2. Überarbeitungsdatum
    'Überarbeitung':  ['überarbeit', 'änderung', 'revision', 'bearbeitung', 'quick-fds', 'version'],
    #3. Datum alte Version
    'Vorgänger':  ['ersetzt', 'ersatz', 'fassung', 'letzten'],
    #4. Gültigkeitsdatum
    'Gültig':  ['kraft', 'freigabe'],
    #5. Negative Exceptions
    'Exclude': ['sblcore', 'artikel']
    #6. All other not explicit listed cases are also printdate
}

#Preprocessing
data ['word'] = data ['word'].astype(str)
#Convert all to lower case
data ['word'] = data['word'].str.lower()

#Add new columns for feature generation
data['date_nr'] = np.nan
data['date_string'] = np.nan
data['date_cat'] = np.nan
data['date_stopword'] = np.nan

#Filter out special characters for simpler trigger detection
# & (data['Page'] == 1)
data_iter = pd.DataFrame(data.loc[(data['special_char'] <1)])
#Update work index + save old index
data_iter.reset_index(inplace=True)


#Iterrate through dataframe
for row in data_iter.itertuples(index=True):
    print (row.doc, row.Index)
    # Catch exception with subchapter numbers
    if row.word.endswith('.0'):
        continue
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
                '%d. %b %y', '%d %b %y', '%d. %B %y', '%d %B %y', '%w. %b %y', '%w %b %y', '%w. %B %y', '%w %B %y'
                ):
        try:
            s = str(row.word)
            
            #Try to parse string in date
            date = datetime.strptime(s, fmt).date()

            #Prevent picking wrong dates
            if date < date.today():
                org_index = int(data_iter.loc[row.Index, 'index'])
                data.loc[org_index, 'date_nr'] = date
                #Catch 5 words before date
                date_str = ''
                for i in range(5,0,-1): 
                    date_str += data_iter.loc[row.Index-i, 'word'] + ' '
                data.loc[org_index, 'date_string'] = date_str

                #search in string for label key words
                temp = []
                for key, value in date_labels.items ():
                    for i in value:
                        temp.append((key, date_str.find(i)))
                #if substring was found value is >= 0
                if max(temp, key=itemgetter(1))[1] >= 0:
                    date_label = max(temp, key=itemgetter(1))[0]

                else:
                    date_label = 'Druck_implizit'
                # create label in working csv
                data.loc[org_index, 'date_cat'] = date_label

                # Add stopword label
                stop = False
                for i in range (1,6):
                    if stop == True:
                        break
                    for key, value in date_labels.items ():
                            for j in value:
                                if data_iter.loc[row.Index-i, 'word'].find(j) != -1:
                                    data.loc[int(data_iter.loc[row.Index-i, 'index']),'date_stopword'] = key
                                    stop = True
            break

        except (ValueError, TypeError) as e:
            continue

data.to_csv(datapath + 'dates_all_identified_ap.csv', encoding='utf-8-sig')

