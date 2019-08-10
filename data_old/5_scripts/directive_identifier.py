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
data = pd.read_csv(datapath + 'data_all_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Labels
reach_id = ['1907/2006', '2015/830']

#Preprocessing
data ['word'] = data ['word'].astype(str)
#data ['word'] = data['word'].str.lower()

#Add new colum for reach status
data['directive'] = np.nan


#Loop through all rows in data
for row in data.loc[data['Page'] <= 2, ['word']].itertuples(index=True):
    #search for reach_id
    for rid in reach_id:
        if row.word.find(rid) != -1:
            data.loc[row.Index, 'directive'] = 1
    
data.to_csv('directive_identified.csv', encoding='utf-8-sig')