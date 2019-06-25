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
data = pd.read_csv(datapath + 'usecase_identified_part.csv', encoding='utf-8-sig', index_col=0)

#Labels
usecase_start = ['abgeraten wird']
usecase_stop = ['einzelheiten zum', 'angaben des lieferanten']
trigger_start = [
                'empfohlene r verwendungszweck e', 
                'identifizierte Verwendungen des stoffs oder gemischs',
                'identifizierte verwendungen', 
                'verwendung des stoffes des gemisches', 
                'verwendung des stoffs des gemischs',
                'funktions- oder verwendungskategorie',
                'verwendungen von denen abgeraten wird',
                'vorgesehene Verwendung',
                'abgeratene verwendungen'
                ]

trigger_end = [
                'kontaktieren sie ihren lieferanten für weitere informationen',
                'zur Zeit liegen keine Informationen hierzu vor', 
                'keine weiteren relevanten informationen verfügbar',
                '1.3 einzelheiten zum',
                '1.3 einzelheiten zum',
                'einzelheiten zum', 
                'angaben des lieferanten'
                ]
#ignore_list = ['zur Zeit liegen keine Informationen hierzu vor', 'keine weiteren relevanten informationen verfügbar']




#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()
data = data.drop(['Page', 'Ycord_first', 'Xcord_first', 'font_size', 'font_name', 'Object', 'Textbox', 'ycord_average'], axis=1)

print (data.head())

#Add new column for part string
data['usecase'] = np.nan

data_iter = pd.DataFrame(data.loc[data['special_char'] <1])
#Update work index + save old index
data_iter.reset_index(inplace=True)

index = 10
length = len(data_iter['index'])-1

while index < length:
    # Print output
    row = data_iter.loc[index, :]
    print (index, row.word)

    # Create sliding string window of next 10 words
    window = ''
    for i in range (-10,1):
        window = window + ' ' + data_iter.loc[index+i, 'word']
    
    for trig_st in trigger_start:
        if window.find(trig_st) != -1:
            keepsearching = True
            detect_end = ''
            k = index + 10
            while keepsearching:
                k +=1
                detect_end = detect_end + ' ' + data_iter.loc[k, 'word']

                for trig_en in trigger_end:
                    if detect_end.find(trig_en) != -1:
                        end_index = k-len(trig_en.split())
                        org_index1 = int(data_iter.loc[j+1, 'index'])
                        org_index2 = int(data_iter.loc[end_index, 'index'])
                        data.loc[org_index1:org_index2, 'usecase_sep'] = 1
                        index = end_index
                        keepsearching = False
                        break
            break
    index +=1

data.to_csv(datapath + 'usecase_identified_sep.csv', encoding='utf-8-sig')