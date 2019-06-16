import pandas as pd
import numpy as np
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
reach_id = ['1907/2006', '2015/830']

#Preprocessing
data ['word'] = data ['word'].astype(str)
#data ['word'] = data['word'].str.lower()

#Add new colum for reach status
data['isreach'] = np.nan


#Loop through all rows in data
for row in data.loc[data['Page'] <= 2, ['word']].itertuples(index=True):
    print (row)
    #search for reach_id
    for rid in reach_id:
        if row.word.find(rid) != -1:
            data.loc[row.Index, 'isreach'] = 1
    
data.to_csv(datapath + 'directive_identified.csv', encoding='utf-8-sig')