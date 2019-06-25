import pandas as pd
import numpy as np
import os 
import re
from operator import itemgetter
import re

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'
chemicals_dir = 'data/4_chemicals/'

#full path to data files
datapath = os.path.join(ospath, datadir)
chempath = os.path.join(ospath, chemicals_dir)

#read raw data csv
data = pd.read_csv(datapath + 'data_all_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Add new colum for status if word is part of company name
data['chem'] = np.nan

#read chemicals data csv
chem = pd.read_csv(chempath + 'chemicals.csv')

cas = list(chem['CAS number'])

stop_list = ['ABSCHNITT','Erste-Hilfe-Maßnahmen']

'''
filter out relevant data (only data in chapter 3.2)
'''

cas_continue_list = ['Skin','Eye','ABSCHNITT','EINECS']

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
#data['Full Index'] = data.index

# keep only chapter data
#data = data[data['chapter 3.2'] == 1]

#reset index
#data = data.reset_index(drop = True)

data = data[:90000]
doc = ''

# use regex to identify CAS numbers
for row in data.loc[data['chapter 3.2'] == 1, ['word']].itertuples(index=True):
    #regex
    if re.match(r"\d{4}-\d{2}-\d{1}$", str(row.word)) or re.match(r"\d{3}-\d{2}-\d{1}$", str(row.word)) or re.match(r"\d{5}-\d{2}-\d{1}$", str(row.word)) or re.match(r"\d{6}-\d{2}-\d{1}$", str(row.word)):

        # check if start of new doc
        if data.loc[row.Index, 'doc'] != doc:
            i = 1
        doc = data.loc[row.Index, 'doc']

        data.loc[row.Index, 'chem'] = 'cas_' + str(i)


        #look for % in both directions
        j = 0

        #check for words in the same line
        while True:
            j += 1

            if data.loc[row.Index-2,'word'] == '-':
                data.loc[row.Index -1:row.Index -3 ,'chem_%'] = 'cas' + str(i)
                break

            if data.loc[row.Index+1,'word'] == '%':
                data.loc[row.Index + 3, 'chem_%'] = 'cas' + str(i)
                break

            if data.loc[row.Index+j,'word'] == '<':
                data.loc[row.Index +j:row.Index +j + 1, 'chem_%'] = 'cas' + str(i)
                break

            #look for % ratio around CAS number
            if data.loc[row.Index-j,'word'] == '%':
                data.loc[row.Index -j, 'chem_%'] = 'cas' + str(i)

                #Look for all the digits assigned to the % symbol
                t = 0
                while True:
                    t += 1
                    # stop if '<'
                    if data.loc[row.Index -j -t, 'word'] == '<':
                        # if <, check if token before '-' --> also range --> take token before as well
                        if data.loc[row.Index -j -t - 1, 'word'] == '-':
                            print(row.Index)
                            data.loc[row.Index - j - t - 2:row.Index-j, 'chem_%'] = 'cas' + str(i)
                        else:
                            data.loc[row.Index - j - t:row.Index-j, 'chem_%'] = 'cas' + str(i)
                        break
                    # i '-' found: range --> label until one token before '-'
                    if data.loc[row.Index -j -t, 'word'] == '-':
                        data.loc[row.Index - j - (t+1):row.Index-j, 'chem_%'] = 'cas' + str(i)
                        break
                    #stop is looking for more than 10 tokens
                    if t == 10:
                        data.loc[row.Index -j -1, 'chem_%'] = 'cas' + str(i)
                        break
                   

                break

            if data.loc[row.Index+j,'word'] == '%':
                data.loc[row.Index +j, 'chem_%'] = 'cas' + str(i)

                #Look for all the digits assigned to the % symbol
                t = 1 
                while True:
                    # if '<' 
                    if data.loc[row.Index +j -t, 'word'] == '<':
                        # if <, check if token before '-' --> also range --> take token before as well
                        if data.loc[row.Index +j -t - 1, 'word'] == '-':
                            print(row.Index)
                            data.loc[row.Index + j - t - 2:row.Index+j, 'chem_%'] = 'cas' + str(i)
                        else:
                            data.loc[row.Index + j - t:row.Index+j, 'chem_%'] = 'cas' + str(i)
                        break
                    # i '-' found: range --> label until one token before '-'
                    if data.loc[row.Index +j -t, 'word'] == '-':
                        data.loc[row.Index + j - (t+1):row.Index-j, 'chem_%'] = 'cas' + str(i)
                        break

                    #stop is looking for more than 10 tokens
                    if t == 10:
                        data.loc[row.Index +j -1, 'chem_%'] = 'cas' + str(i)
                        break
                    
                    t += 1

                break

            

        i += 1


        #look for word around CAS number to identify name of chemical element
        #in most of the cases: name after CAS number

       # i = 1

 ##           while True:
  #                i += 1
   #             if data.loc[row.Index, 'word'] = 


data.to_csv('chem_identified.csv', index=False, encoding='utf-8-sig')


#data['chem'] = data['word'].apply(lambda x)

