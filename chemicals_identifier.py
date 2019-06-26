import pandas as pd
import numpy as np
import os 
import re
from operator import itemgetter
import re
import csv

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

with open(chempath + 'cas_chemical_mapping.csv') as f:
    next(f)  # Skip the header
    reader = csv.reader(f, skipinitialspace=True)
    cas_mapping = dict(reader)

print(cas_mapping)

#Add new colum for status if word is part of company name
data['chem'] = np.nan
data['chem_name'] = np.nan

#read chemicals data csv
chem = pd.read_csv(chempath + 'chemicals.csv')

cas = list(chem['CAS number'])

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

#data = data[:90000]
doc = ''

# use regex to identify CAS numbers
for row in data.loc[data['chapter 3.2'] == 1, ['word']].itertuples(index=True):
    #regex
    if re.match(r"\d{4}-\d{2}-\d{1}$", str(row.word)) or re.match(r"\d{3}-\d{2}-\d{1}$", str(row.word)) or re.match(r"\d{5}-\d{2}-\d{1}$", str(row.word)) or re.match(r"\d{6}-\d{2}-\d{1}$", str(row.word)):

        # check if start of new doc
        if data.loc[row.Index, 'doc'] != doc:
            i = 1
        doc = data.loc[row.Index, 'doc']

        #label cas nr according to current document
        data.loc[row.Index, 'chem'] = 'cas_' + str(i)

        #save cas nr
        cas_nr = str(row.word)
        #look in dict for corresponding name of cas nr
        cas_name = str(cas_mapping[cas_nr])

        # look for cas names in both directions
        for k in range (30):
            #current tokens for both directions
            token_down = str(data.loc[row.Index+k,'word']).lower()
            token_up = str(data.loc[row.Index-k,'word']).lower()

            # if token is substring of cas_name --> label as name (only if len >2 or digit)
            if token_down in cas_name.lower() and len(token_down) > 2:
                data.loc[row.Index+k, 'chem_name'] = 'cas_' + str(i) + '_name'
            # if not: check if substrings of token with len of 3 occur in cas_name
            elif len(token_down) > 3:
                sliding_tokens = [token_down[i:i+4] for i in range(len(token_down)-3)]
                if any(token in cas_name.lower() for token in sliding_tokens):
                    data.loc[row.Index+k, 'chem_name'] = 'cas_' + str(i) + '_name'

            # if token is substring of cas_name --> label as name (only if len >2 or digit)
            if token_up in cas_name.lower() and len(token_up) > 2:
                data.loc[row.Index-k, 'chem_name'] = 'cas_' + str(i) + '_name'
             # if not: check if substrings of token with len of 3 occur in cas_name
            elif len(token_up) > 3:
                sliding_tokens = [token_up[i:i+4] for i in range(len(token_up)-3)]
                if any(token in cas_name.lower() for token in sliding_tokens):
                    data.loc[row.Index-k, 'chem_name'] = 'cas_' + str(i) + '_name'

        #look for % and ranges in both directions
        j = 0

        while True:
            j += 1

            #sd 47, 57, 61, 82, 98

            if j == 100:
                break
            
            if data.loc[row.Index-2,'word'] == '-':
                data.loc[row.Index -3:row.Index -1 ,'chem_%'] = 'cas' + str(i)
                break

            if data.loc[row.Index+2,'word'] == '-':
                print(row.Index)
                data.loc[row.Index +1:row.Index + 3 ,'chem_%'] = 'cas' + str(i)
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
                    if data.loc[row.Index -j -t, 'word'] == '<' or '≤':
                        # if <, check if token before '-' --> also range --> take token before as well
                        if data.loc[row.Index -j -t - 1, 'word'] == '-':
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
                    if data.loc[row.Index +j -t, 'word'] == '<' or '≤':
                        # if <, check if token before '-' --> also range --> take token before as well
                        if data.loc[row.Index +j -t - 1, 'word'] == '-':
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


data.to_csv('chem_identified.csv', index=False, encoding='utf-8-sig')

