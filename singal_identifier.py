
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
data = pd.read_csv(datapath + 'test.csv', encoding='utf-8-sig', index_col=0)

#Labels
reach_id = ['signalwort']
reach_range = ['achtung', 'warnung', 'gefahr', 'entfällt']

#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()

#Add new colum for reach status
data['signal'] = np.nan

#Filter out special characters for simpler trigger detection
data_iter = pd.DataFrame(data.loc[data['special_char2'] <1])
#Update work index + save old index
data_iter.reset_index(inplace=True)

#Loop through all rows in data
for row in data_iter.itertuples(index=True):
    print (row.Index, row.word)
    #search for reach_id
    for rid in reach_id:
        if row.word.find(rid) != -1:
            i = 0
            keepsearching = True
            while keepsearching:
                i +=1
                signal = data_iter.loc[row.Index+i, 'word']
                for rng in reach_range:
                    if rng == signal:
                        temp = int(data_iter.loc[row.Index+i, 'index'])
                        data.loc[temp, 'signal'] = 1
                        keepsearching = False

data.to_csv(datapath + 'signal_identified.csv', encoding='utf-8-sig')