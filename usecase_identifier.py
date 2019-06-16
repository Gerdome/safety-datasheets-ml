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
usecase_start = ['abgeraten wird']
usecase_stop = ['einzelheiten zum', 'angaben des lieferanteng']

#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()

#Add new column for part string
data['usecase_part'] = np.nan
#Add new column for advised usecase
data['usecase_pro'] = np.nan
#Adde new column for unadvised usecase
data['usecase_con'] = np.nan

part_found = False


index = 1
while index < len(data.index):
    row = data.loc[index, :]
    print (index, row.word)
    start_str = data.loc[index-1, 'word'] + ' ' + row.word

    #search for starting point
    for start in usecase_start:
        if start in start_str:
            #start from here building string
            usecase_str = ''

            #add words till stop
            i = 0
            while True:
                i += 1
                recording = True
                stop_str = data.loc[index+i+1,'word'] + ' ' + data.loc[index+i+2,'word']
                for stop in usecase_stop:
                    if stop in stop_str:
                        recording=False
                if recording == False:
                    break
                usecase_str = usecase_str + ' ' + data.loc[index+i, 'word']
            #data.loc[index:index+i, 'usecase_part'] = usecase_str
            data.loc[index+i, 'usecase_part'] = usecase_str
            index += i
        
        #separte generated string



        break
    index +=1

data.to_csv(datapath + 'usecase_identified_while.csv', encoding='utf-8-sig')




'''
for row in data.loc[data['Page'] <= 2, ['word']].itertuples(index=True):
    start_str = ''
    print (row)
    if row.Index >0:
        start_str = data.loc[row.Index-1, 'word'] + ' ' + row.word
    
    #search for starting point
    for start in usecase_start:
        if start in start_str:
            #start from here building string
            usecase_str = ''

            #add words till stop
            i = 0
            while True:
                i += 1
                recording = True
                stop_str = data.loc[row.Index+i+1,'word'] + ' ' + data.loc[row.Index+i+2,'word']
                for stop in usecase_stop:
                    if stop in stop_str:
                        recording=False
                if recording == False:
                    break
                usecase_str = usecase_str + ' ' + data.loc[row.Index+i, 'word']
            #data.loc[row.Index:row.Index+i, 'usecase_part'] = usecase_str
            data.loc[row.Index+i, 'usecase_part'] = usecase_str
        break
'''