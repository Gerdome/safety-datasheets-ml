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
data = pd.read_csv(datapath + 'data_all_avg_ordered.csv', encoding='utf-8-sig', index_col=0)

#Labels
legal_forms = ['gmbh', 'ug', 'ag', 'gbr', 'e.k.', 'ohg', 'ohg', 'kg', 'se', 'lp', 'llp', 'llp', 'lllp', 'llc', 'lc', 'ltd. co', 'pllc', 'corp.', 'inc.', 'corp', 'inc', 'kluthe', 's.l.', 'bvba']
stop_list = ['firmenname', 'firmenbezeichnung','lieferanschrift', 'lieferant', 'der', ':', ')', 'zum', 'hersteller', 'inverkehrsbringer', '*', 'firma']
exclusion_list = ['vergiftungsinformationszentrale', 'tüv', 'website', 'gbk', '@', 'www']


#Preprocessing
data ['word'] = data ['word'].astype(str)
data ['word'] = data['word'].str.lower()


#Add new column for company name
data['company_name'] = np.nan
#Add new colum for status if word is part of company name
data['company'] = np.nan

#Loop through all rows in data
for row in data.loc[data['Page'] <= 2, ['word']].itertuples(index=True):
    print (row)
    #search for legal form
    for lf in legal_forms:
        if lf in row.word:
            #start from here building string
            company_str = row.word
            i = 0

            #help variable for exluded string
            excluded_str =False

            #check for words in the same line
            while True:
                i += 1
                #help variable for stop word search
                stop_word = False
                #check line of previous word
                if data.loc[row.Index-i,'ycord_average'] != data.loc[row.Index,'ycord_average']:
                    break
                #check stop list
                for stp in stop_list:
                    if stp in data.loc[row.Index-i,'word']:
                        stop_word = True
                        #break from inner stp loop
                        break
                #check exclusion list
                for el in exclusion_list: 
                    if (data.loc[row.Index-i,'word'].find(el) != -1) or (company_str.find(el) != -1):
                        excluded_str = True
                        #break from inner el loop
                        break
                
                #break from outer while loop
                if stop_word == True:
                    break
                #Add word to string
                company_str += ' ' + data.loc[row.Index-i,'word']
            
            if excluded_str == False:
                #Reverse order of strings
                company_str_r = ' '.join(company_str.split(" ")[-1::-1])
                #Set value for extracted company name
                data.loc[row.Index-i+1:row.Index, 'company_name'] = company_str_r
                #Set indicator if word is part of company name
                data.loc[row.Index-i+1:row.Index+1, 'company'] = 1
        #break from outer lf loop        
        break
    
data.to_csv(datapath + 'company_identified.csv', encoding='utf-8-sig')