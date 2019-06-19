import pandas as pd
import numpy as np
import os 
import re

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_all_avg_ordered.csv', dtype=str, index_col = 0)

#Add new colum for status if word is part of company name
data['subchapter'] = np.nan

subschapter = ( '1.1','1.2','1.3','1.4',
                '2.1','2.2','2.3',
                '3.1','3.2',
                '1.1.','1.2.','1.3.','1.4.',
                '2.1.','2.2.','2.3.',
                '3.1.','3.2.',            
                )

subchapter_first_words = [['Produktidentifikator'], #1.1        -0 
                        ['Relevante','identifizierte'], #1.2    -1
                        ['Einzelheiten','zum'], #1.3            -2
                        ['Notrufnummer'],  #1.4             -3
                        ['Einstufung','des'],  #2.1             -4
                        ['Kennzeichnungselemente'], #2.2     -5
                        ['Sonstige','Gefahren'], #2.3           -6
                        ['Stoffe'], #3.1                        -7
                        ['Gemische']]  #3.2                     -8

subchapter_last_words = [['Produktidentifikator'], #1.1         -0 
                        ['wird'], #1.2                          -1
                        ['bereitstellt'], #1.3                -2
                        ['Notrufnummer'],  #1.4                 -3
                        ['Gemischs','Gemisches'],  #2.1         -4
                        ['Kennzeichnungselemente'], #2.2        -5
                        ['Gefahren'], #2.3                      -6
                        ['Stoffe'], #3.1                        -7
                        ['Gemische']]  #3.2                     -8

#Last words of subchapter headers as stop words
stop_list = ['Produktidentifikator','1272/2008','bereitstellt','Notrufnummer', 'Gemisches','Gemischs','Kennzeichnungselemente']



#Loop through all rows in data
for row in data.loc[:, ['word']].itertuples(index=True):
    #either subchapter numbers 
    if row.word in subschapter:

        #first token of subchapter header 
        
        i = 0

        #check until word is not in the same format and font size 
        while True:
            i += 1

            #help variable for stop word search
            stop_word = False

            # if last word of header --> break
            for stp in stop_list:
                if stp == data.loc[row.Index + i,'word']:
                    stop_word = True
                    #break from inner stp loop
                    break

            #break from outer while loop
            if stop_word == True:
                break

            # if word is in different format --> end of header
            # comapere with Index + 1 (skip in this case the number, since number is often smaller font size or not bold)
            if data.loc[row.Index+i,'font_name'] != data.loc[row.Index + 1,'font_name'] or data.loc[row.Index+i,'font_size'] != data.loc[row.Index + 1,'font_size']:  
                #i - 1 because word with different format is not part of header
                i = i - 1
                break
                            
        #Set indicator if word is part of chapter label
        data.loc[row.Index:row.Index+(i), 'subchapter'] = 1

    else:
        # if no number for subchapter availabe --> look for words
        for w in range(9):
            #sometimes only one word long
            if w in (0,3,5,7,8):
                if row.word == subchapter_first_words[w][0] and 'Bold' in data.loc[row.Index,'font_name']:
                    #Set indicator if word is part of chapter label
                    data.loc[row.Index, 'subchapter'] = 1

            # sometimes more than one word       
            elif w in (1,2,4,6):
                if row.word == subchapter_first_words[w][0] and data.loc[row.Index+1,'word'] == subchapter_first_words[w][1] and 'Bold' in data.loc[row.Index,'font_name']:
                    i = 0
                    while True:
                        i += 1

                        #help variable for stop word search
                        stop_word = False
                        # if last word of header --> break
                        if w == 4:
                            if data.loc[row.Index+i,'word'] == subchapter_last_words[w][0] or data.loc[row.Index+i,'word'] == subchapter_last_words[w][1]:
                                stop_word = True
                        else:
                            if data.loc[row.Index+i,'word'] == subchapter_last_words[w][0]:
                                stop_word = True
                        #break from outer while loop
                        if stop_word == True:
                            break

                        if data.loc[row.Index+i,'font_name'] != data.loc[row.Index,'font_name'] or data.loc[row.Index+i,'font_size'] != data.loc[row.Index,'font_size']:  
                            #i - 1 because word with different format is not part of header
                            i = i - 1
                            break

                    #Set indicator if word is part of chapter label
                    data.loc[row.Index:row.Index+(i), 'subchapter'] = 1
        


data.to_csv('subchapter_identified.csv', encoding='utf-8-sig')


