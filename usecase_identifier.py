import pandas as pd
import numpy as np
import os 
import re
from operator import itemgetter

def remove_substr(substr, str):
    index = 0
    length = len(substr)
    while str.find(substr) != -1:
        index = str.find(substr)
        str = str[0:index] + str[index+length:]
    return str

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Labels
usecase_start = ['abgeraten wird']
usecase_stop = ['einzelheiten zum', 'angaben des lieferanteng']
usecase_pro_start = ['empfohlene ( r ) verwendungszweck ( e )', 
                    'identifizierte Verwendungen des stoffs oder gemischs',
                    'identifizierte verwendungen', 
                    'verwendung des stoffes / des gemisches', 
                    'verwendung des stoffs/des gemischs',
                    'funktions- oder verwendungskategorie']
usecase_con_start = ['verwendungen, von denen abgeraten wird',
                    'abgeratene verwendungen']
ignore_list = ['zur Zeit liegen keine Informationen hierzu vor.', 'keine weiteren relevanten informationen verfügbar']




#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()

#Add new column for part string
data['usecase_part'] = np.nan
#Add new column for advised usecase
data['usecase_pro'] = np.nan
#Adde new column for unadvised usecase
data['usecase_con'] = np.nan

data['usecase_part_clean'] = np.nan

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
        
            #clean separated string
            for ign in ignore_list:
                if ign in usecase_str:
                    usecase_str = remove_substr(ign, usecase_str)
                    data.loc[index+i, 'usecase_part_clean'] = usecase_str
            
            #separte generated string
            


        break
    index +=1

data.to_csv(datapath + 'usecase_identified_prep.csv', encoding='utf-8-sig')













'''

usecase_start = ['abgeraten wird']
usecase_stop = ['einzelheiten zum', 'angaben des lieferanten']
usecase_pro_start = ['empfohlener verwendungszwecke', 
                    'identifizierte Verwendungen des stoffs oder gemischs',
                    'identifizierte verwendungen', 
                    'verwendung des stoffes des gemisches', 
                    'verwendung des stoffs des gemischs',
                    'funktions oder verwendungskategorie']
usecase_con_start = ['verwendungen, von denen abgeraten wird',
                    'abgeratene verwendungen']
ignore_list = ['zur Zeit liegen keine Informationen hierzu vor', 'keine weiteren relevanten informationen verfügbar']




data_iter = pd.DataFrame(data.loc[data['special_char'] <1])

#Update work index + save old index
data_iter.reset_index(inplace=True)

counter = 0
for row in data_iter.itertuples(index=True):
    if row.Index == counter: 
        start_str = ''
        print (row.Index, row.word)
        if row.Index >0:
            start_str = data_iter.loc[row.Index-1, 'word'] + ' ' + row.word
        
        usecase_str = ''
        #search for starting point
        for start in usecase_start:
            #start from here building string
            if start in start_str:
                #add words till stop
                i = 0
                while True:
                    i += 1
                    recording = True
                    stop_str = data_iter.loc[row.Index+i+1,'word'] + ' ' + data_iter.loc[row.Index+i+2,'word']
                    for stop in usecase_stop:
                        if stop in stop_str:
                            recording=False
                    if recording == False:
                        break
                    usecase_str = usecase_str + ' ' + data_iter.loc[row.Index+i, 'word']
                temp_org_index = int (data_iter.loc[row.Index+i, 'index'])
                data.loc[temp_org_index, 'usecase_part'] = usecase_str
                counter += i-1
            break
        
        if usecase_str != '':
            #clean separated string
            for ign in ignore_list:
                if ign in usecase_str:
                    usecase_str = remove_substr(ign, usecase_str)
                    data.loc[row.Index+i, 'usecase_part_clean'] = usecase_str
            
            #find starting point of usecase pro or con
    counter +=1




'''

