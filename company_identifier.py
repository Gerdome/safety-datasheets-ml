import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import numpy as np
import os 
import re
from operator import itemgetter

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'labeled/dates+chapter_identified_0_50.csv', dtype=str, encoding='utf-8-sig', index_col=0)

print (data.head())
#Labels
legal_forms = ['gmbh', 'ug', 'ag', 'gbr', 'e.k.', 'ohg', 'ohg', 'kg', 'se', 'lp', 'llp', 'llp', 'lllp', 'llc', 'lc', 'ltd. co', 'pllc', 'corp.', 'inc.']
#['GmbH', 'UG', 'AG', 'GbR', 'e.K.', 'OHG', 'ohg', 'KG', 'SE', 'LP', 'LLP', 'LLP', 'LLLP', 'LLC', 'LC', 'Ltd. Co', 'PLLC', 'Corp.', 'Inc.']

#Preprocessing
data ['word'] = data['word'].str.lower()
#Delete empty cells
data ['word'] = data['word'].replace('', np.nan)
data.dropna(subset=['word'],inplace=True)

#Update work index + save old index
data.reset_index(inplace=True)

#Add new columns for feature generation
data['company_name'] = np.nan

# List for data aggregation
indexlabel_list = []

print ('test')

print (data.head())
print (data.word)

#Iterrate through dataframe
for row in data.loc[data['Page'] == 1, ['word']].itertuples(index=True):
    print (row)
    print('test')
    

#Create separate file with working data and detected labels
#data.to_csv(datapath + 'labeled/company_identified_0_50_.csv', encoding='utf-8-sig')

print ('ende')


'''
print ('schleife')
    for lf in legal_forms:
        if lf in row.word:
            #Catch 5 words before date
            company_str = ''
            for i in range(5,-1,-1):
                company_str += str(data.loc[row.Index-i, 'word']) + ' '
            data.loc[row.Index, 'company_name'] = company_str
            # save label in list for final data
            indexlabel_list.append((int(data.loc[row.Index, 'index']), company_str))


# match labels with final data: fill in identified labels in data
final_data = pd.read_csv(datapath + 'chapter_identified.csv', encoding='utf-8-sig', index_col=0)


for i in indexlabel_list:
    if final_data.loc[i[0],'label'] != '0':
        print ('!!!!!!!!!!!!!!!!' + i[1])
    else:
        print (i)
        final_data.loc[i[0],'label'] = i[1]

final_data.to_csv(os.path.join(ospath, 'data/labeled/dates+chapter_identified_0_50_.csv'), encoding='utf-8-sig')
'''