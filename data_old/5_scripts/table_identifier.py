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

#Add new colum for status if word is part of company name
data['table'] = np.nan

stop_list = ['ABSCHNITT','Erste-Hilfe-Maßnahmen']

'''
filter out relevant data (only data in chapter 3.2)
'''

for row in data.loc[:, ['word']].itertuples(index=True):

    #search for start of chapter 3.2
    if row.word == '3.2' or row.word == '3.2.' or (row.word == 'Zusammensetzung' and data.loc[row.Index + 1,'word'] == '/' and str(data.loc[row.Index + -1,'word']) == '3'):
        #first word of 3.2
        i = 0
        while True:
            i += 1
            
            #help variable for stop word search
            stop_word = False

            # if beginning of subchapter --> end of header
            for stp in stop_list:
                if stp == data.loc[row.Index + i,'word']:
                    stop_word = True
                    #break from inner stp loop
                    break

            #break from outer while loop
            if stop_word == True:
                break

        #Set indicator if word is part of chapter label
        data.loc[row.Index:row.Index+(i-1), 'chapter 3.2'] = 1

# save old Index in new column
data['Full Index'] = data.index

# keep only chapter data
data = data[data['chapter 3.2'] == 1]

#reset index
data = data.reset_index(drop = True)

'''
identify tables more precise
'''
# delete information on top of table: indicator for start of table is multiple textboxes within same line of text

# iterate through y_cords (lines)
for row in data.loc[:118000, ['Object','ycord_average','table']].itertuples(index=True):
    
    #skip rows that are already labeled --> if already 0 or 1
    if data.loc[row.Index, 'table'] == 0 or data.loc[row.Index, 'table'] == 1:
        continue

    i = 0
    table_identifier = 0
    while True:
        i += 1

        # if new line: break
        if data.loc[row.Index+i,'ycord_average'] != data.loc[row.Index,'ycord_average']:
            break
        
        # as soon as different textbox detected in same line --> table identified
        if data.loc[row.Index+i,'Object'] != data.loc[row.Index,'Object']:
            table_identifier = 1
        
    #Set indicator if words are are part of table
    data.loc[row.Index:row.Index+(i-1), 'table'] = table_identifier

# some lines within a table (e.g. some cells over multiple lines) have the same textbox 
# check if same textbox is somewhere assigned to table --> also assign word to table 

also_table  = []

# function to check
def level_of_detail(x):
    if x.doc == row.doc and x.Page == row.Page and x.Object == row.Object:
        also_table.append(x['Full Index'])


# iterate through words again
for row in data.loc[:, ['Object','word','doc','Page','table']].itertuples(index=True):
    # only interested in words assigned to table 
    if row.table == 0:
        continue
    #data['also_table'] = data[['Object','word','doc','Page']].apply(lambda x: 0 if x.word == 'hat' else 1 , axis = 1)
    data[['Object','word','doc','Page','Full Index']].apply(level_of_detail, axis = 1)


also_table = list(set(also_table))

data.loc[data['Full Index'].isin(also_table), 'table'] = 1



# textboxes detected by pdfminer helpful --> order not by x/y coordinate --> order by textboxes

data.to_csv('table_identified.csv', encoding='utf-8-sig')

