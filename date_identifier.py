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
data = pd.read_csv(datapath + 'reduced_columns.csv', encoding='utf-8-sig', index_col=0)

#Labels
date_labels = {
    #1. Druckdatum/Erstellung
    'Druck':  ['druck', 'ausgabe', 'ausstellung'],
    #2. Überarbeitungsdatum
    'Überarbeitung':  ['überarbeit', 'änderung', 'revision', 'bearbeitung'],
    #3. Datum alte Version
    'Vorgänger':  ['ersetzt', 'ersatz', 'fassung'],
    #4. Gültigkeitsdatum
    'Gültig':  ['kraft'],
    #5. Nicht zuordbar
}

#Preprocessing
#Convert all to lower case
data ['word'] = data['word'].str.lower()
#Delete non-alpha numeric values at begining and end of words
data ['word'] = data['word'].replace(r"^\W+|\W+$", "", regex=True)

#Update work index + save old index
data.reset_index(inplace=True)

#Add new columns for feature generation
data['date_nr'] = np.nan
data['date_string'] = np.nan
data['date_cat'] = np.nan

# List for data aggregation
indexlabel_list = []

#Iterrate through dataframe
for row in data.loc[data['Page'] == 1, ['word']].itertuples(index=True):
    print (row)
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
                data.loc[row.Index, 'date_nr'] = date
                #Catch 5 words before date
                date_str = ''
                for i in range(5,0,-1): 
                    date_str += str(data.loc[row.Index-i, 'word']) + ' '
                data.loc[row.Index, 'date_string'] = date_str

                #search in string for label key words
                temp = []
                for key, value in date_labels.items ():
                    for i in value:
                        temp.append((key, date_str.find(i)))
                #if substring was found value is >= 0
                if max(temp, key=itemgetter(1))[1] >= 0:
                    date_label = max(temp, key=itemgetter(1))[0]
                else:
                    date_label = 'Nicht zuordbar'
                # create label in working csv
                data.loc[row.Index, 'date_cat'] = date_label
                # save label in list for final data
                indexlabel_list.append((int(data.loc[row.Index, 'index']), date_label))
            break

        except (ValueError, TypeError) as e:
            continue

#Create separate file with working data and detected labels
#data.to_csv(os.path.join(ospath, 'data/labeled/dates_identified_0_50_.csv'), encoding='utf-8-sig')


# match labels with final data: fill in identified labels in data
final_data = pd.read_csv(datapath + 'reduced_columns.csv', encoding='utf-8-sig', index_col=0)

# Create label column
data['dates'] = np.nan

for i in indexlabel_list:
        final_data.loc[i[0],'dates'] = i[1]

#Delete after test
#final_data.drop(['Ycord_first','Object','Textbox'], axis=1)

final_data.to_csv(datapath + 'dates_identified_0_50.csv', encoding='utf-8-sig')