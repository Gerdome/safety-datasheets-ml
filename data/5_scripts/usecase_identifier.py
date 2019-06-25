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
data = pd.read_csv(datapath + 'data_all_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Labels
# Detects start and end of the whole usecase part
usecase_start = ['abgeraten wird']
usecase_stop = ['einzelheiten zum', 
                '1.3. angaben',
                '1.3 angaben',
                'angaben des'
                ]

# Detects the starting points within the usecasepart of pro usecases (=1) and con usecases (=0)
trigger_start = [
                ('empfohlene r verwendungszweck e', 1),
                ('verwendung des stoffes oder des gemisches', 1), 
                ('verwendung des stoffs oder des gemischs', 1),
                ('verwendung des stoffes oder gemisches', 1), 
                ('verwendung des stoffs oder gemischs', 1),
                ('verwendung des stoffes des gemisches', 1), 
                ('verwendung des stoffs des gemischs',1),
                ('identifizierte verwendungen', 1),
                ('verwendungen von denen abgeraten wird', 0),
                ('vorgesehene verwendung', 0),
                ('abgeratene verwendungen', 0)
                ]
# Detects the ending points within the usecasepart of pro usecases (=1) and con usecases (=0) // Note: new usecase introduction could be endingpoint of previous usecase section
trigger_end = [
                'empfohlene r verwendungszweck e',
                'verwendung des stoffes oder des gemisches', 
                'verwendung des stoffs oder des gemischs',
                'verwendung des stoffes oder gemisches', 
                'verwendung des stoffs oder gemischs',
                'verwendung des stoffes des gemisches', 
                'verwendung des stoffs des gemischs',
                'identifizierte verwendungen',
                'verwendungen von denen abgeraten wird',
                'vorgesehene verwendung',
                'abgeratene verwendungen',

                'kontaktieren sie ihren lieferanten für weitere informationen',
                'zur Zeit liegen keine Informationen hierzu vor', 
                'keine weiteren relevanten informationen verfügbar',
                '1.2.2. verwendungen',
                '1.3. einzelheiten zum',
                '1.3 einzelheiten zum',
                'einzelheiten zum',
                '1.3. angaben des lieferanten',
                '1.3 angaben des lieferanten', 
                'angaben des lieferanten'
                ]




#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()
#Remove unnecessary columns
data = data.drop(['Page', 'Ycord_first', 'Xcord_first', 'font_size', 'font_name', 'Object', 'Textbox', 'ycord_average'], axis=1)

#Add new column for part string
data['usecase_part'] = np.nan
#Add new column for advised usecase
data['usecase_pro'] = np.nan
#Adde new column for unadvised usecase
data['usecase_con'] = np.nan



#Filter out special characters for simpler trigger detection
data_iter = pd.DataFrame(data.loc[data['special_char'] <1])
#Update work index + save old index
data_iter.reset_index(inplace=True)

#start with index 1 because of sliding window (range = 2)
index = 1

length = len(data_iter['index'])-1

while index < length:
    row = data_iter.loc[index, :]
    docu = row.doc

    # Sliding window of start point
    start_str = data_iter.loc[index-1, 'word'] + ' ' + row.word

    #search for starting point
    for start in usecase_start:
        if start in start_str:
            #start from here building string
            usecase_str = ''

            #add words till stop
            i = index
            while True:
                i += 1
                recording = True
                stop_str = data_iter.loc[i+1,'word'] + ' ' + data_iter.loc[i+2,'word']
                for stop in usecase_stop:
                    if stop in stop_str:
                        recording=False
                if recording == False:
                    break
                usecase_str = usecase_str + ' ' + data_iter.loc[i, 'word']
            # search corresponding index of unfiltered dataframe
            temp1 = int(data_iter.loc[i, 'index'])
            # add usecase string with the whole part to last index of part
            data.loc[temp1-1, 'usecase_part'] = usecase_str
            
            
            #start searching for usecases from this position
            detect_start = ''
            keepsearching = True
            end_index = 0
            j = index+1
            while j < i:
                keepsearching = True
                # build string
                detect_start = detect_start + ' ' + data_iter.loc[j, 'word']

                for trig_st in trigger_start:
                    #if trigger was found start searching for the end of this (sub-)part
                    if detect_start.find(trig_st[0]) != -1:
                        detect_end = ''
                        k = j
                        while keepsearching:
                            k +=1
                            detect_end = detect_end + ' ' + data_iter.loc[k, 'word']

                            for trig_en in trigger_end:
                                # if end trigger was found retunr last index of part
                                if detect_end.find(trig_en) != -1:
                                    # last index of part is overall number of words in the string minus the length of the trigger
                                    end_index = k-len(trig_en.split())
                                    # convert the found range in the range of the unprocessed dataframe
                                    temp2 = int(data_iter.loc[j+1, 'index'])
                                    temp3 = int(data_iter.loc[end_index, 'index'])
                                    # check if part is pro or con usecase
                                    if trig_st[1] == 1:
                                        data.loc[temp2:temp3, 'usecase_pro'] = 1
                                    else:
                                        data.loc[temp2:temp3, 'usecase_con'] = 1
                                    j = end_index
                                    keepsearching = False
                                    detect_start = ''
                                    break
                        break
                j +=1
            index = j
        break
    index +=1

data.to_csv('usecase_identified.csv', encoding='utf-8-sig')