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

subchapter_first_words = {'Produktidentifikator' : '',
                        'Relevante' : 'identifizierte',
                        'Einzelheiten':'zum',
                        'Notrufnummer': '',
                        'Einstufung' : 'des',
                        'Kennzeichnungselemente': '',
                        'Sonstige': 'Gefahren',
                        'Stoffe':''
                        ,'Gemische': ''}

#Last words of subchapter headers as stop words
stop_list = ['Produktidentifikator','1272/2008']



#Loop through all rows in data
for row in data.loc[:90000, ['word']].itertuples(index=True):
    #either subchapter numbers or (first words of subchapter AND and the beginning of the line AND Bold)
    if row.word in subschapter or (row.word in subchapter_first_words and data.loc[row.Index-i,'ycord_average'] != data.loc[row.Index,'ycord_average'] and 'Bold' in data.loc[row.Index,'font_name']):
            print (row)
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

data.to_csv('subchapter_identified.csv', encoding='utf-8-sig')


