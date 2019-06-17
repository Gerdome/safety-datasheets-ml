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
data['chapter'] = np.nan

#Beginning numbers of subchapter as stop words
stop_list = ['1.1', '2.1', '3.1','4.1','5.1','6.1', '7.1', '8.1']

#Loop through all rows in data
for row in data.loc[:, ['word']].itertuples(index=True):
    if row.word == 'ABSCHNITT':
            print (row)
            #first token of chapter header
            i = 0

            #check until word is not in the same format and font size 
            while True:
                i += 1
                
                #help variable for stop word search
                stop_word = False

                # if beginning of subchapter --> end of header
                for stp in stop_list:
                    if stp in data.loc[row.Index + i,'word']:
                        stop_word = True
                        #break from inner stp loop
                        break

                #break from outer while loop
                if stop_word == True:
                    break

                # if word is in different format --> end of header
                if data.loc[row.Index+i,'font_name'] != data.loc[row.Index,'font_name'] or data.loc[row.Index+i,'font_size'] != data.loc[row.Index,'font_size']:  
                    break
                             
            #Set indicator if word is part of chapter label
            data.loc[row.Index:row.Index+(i-1), 'chapter'] = 1

data.to_csv('chapter_identified.csv', encoding='utf-8-sig')

