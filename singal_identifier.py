
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
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Labels
reach_id = ['signalwort', 'warnhinweise']

#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()

#Add new colum for reach status
data['signal'] = np.nan

#Eingelesene Dokumente
docs = data.doc.unique().tolist()
success = []

#Loop through all rows in data
for row in data.loc[data['Page'] <= 2, ['word']].itertuples(index=True):
    print (row)
    #search for reach_id
    for rid in reach_id:
        if row.word.find(rid) != -1:
            i = 1
            while True:
                temp = data.loc[row.Index+i,'word']
                if temp == 'nan' or temp.isalnum() == False:
                    i +=1
                else:
                    data.loc[row.Index+i, 'signal'] = temp
                    success.append(data.loc[row.Index, 'doc'])
                    break

for i in success:
    if i in docs:
        docs.remove(i)

print ('---------------Undetected PDFs-----------------------')

for i in docs:
    print (i)

print ('-----------------Open undected PDFS-------------------')

cmd = 'open $(find ' + ospath + '/data/3_pdf -name '
for i in docs:
    cmd = cmd + i + ' -o -name '
cmd = cmd[:-10] + ')'
print(cmd)


data.to_csv(datapath + 'signal_identified.csv', encoding='utf-8-sig')