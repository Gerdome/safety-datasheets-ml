import pandas as pd
import numpy as np
import os 
import re
from operator import itemgetter
from datetime import datetime
import csv


def prepare_data (filename):
    
    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files
    datapath = os.path.join(ospath, datadir)

    #read raw data csv
    data = pd.read_csv(datapath + filename, encoding='utf-8-sig', index_col = 0)

    #Preprocessing
    data ['word'] = data ['word'].astype(str)
    data ['word_low'] = data['word'].str.lower()

    return data


def create_output (data, filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files
    datapath = os.path.join(ospath, datadir)    

    data.to_csv(datapath + filename, encoding='utf-8-sig')


def chap_identifier (data):
    #Add new colum for status if word is part of company name
    data['chapter'] = np.nan

    chapters = ['1','2','3','4','5','6','7','8',
                '1.','2.','3.','4.','5.','6.','7.','8.']

    chapters_start_words = [':', 'Bezeichnung','Mögliche','Zusammensetzung','Erste-Hilfe-Maßnahmen','Maßnahmen','Handhabung','Begrenzung',
                            'BEZEICHNUNG','MÖGLICHE','ZUSAMMENSETZUNG','ERSTE-HILFE-MAßNAHMEN','MAßNAHMEN','HANDHABUNG','BEGRENZUNG']


    #Beginning numbers of subchapter as stop words
    stop_list = ['1.1', '2.1', '3.1','4.1','5.1','6.1', '7.1', '8.1']

    #Loop through all rows in data
    for row in data.loc[:, ['word']].itertuples(index=True):
        if (row.word == 'ABSCHNITT' and ('Bold' in data.loc[row.Index,'font_name'] or int(data.loc[row.Index,'font_size']) > 10)) or (row.word in chapters and 'Bold' in data.loc[row.Index,'font_name'] and data.loc[row.Index+1,'word'] in chapters_start_words):
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
                data.loc[row.Index:row.Index+(i-1), 'chapter'] = 'chapter'
    return data

def subchapter_identifier (data):
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
                            ['Notrufnummer'],  #1.4                 -3
                            ['Einstufung','des'],  #2.1             -4
                            ['Kennzeichnungselemente'], #2.2        -5
                            ['Sonstige','Gefahren'], #2.3           -6
                            ['Stoffe'], #3.1                        -7
                            ['Gemische']]  #3.2                     -8

    subchapter_last_words = [['Produktidentifikator'], #1.1         -0 
                            ['wird'], #1.2                          -1
                            ['bereitstellt'], #1.3                  -2
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
            data.loc[row.Index:row.Index+(i), 'subchapter'] = 'subchapter'

        else:
            # if no number for subchapter availabe --> look for words
            for w in range(9):
                #sometimes only one word long
                if w in (0,3,5,7,8):
                    if row.word == subchapter_first_words[w][0] and 'Bold' in data.loc[row.Index,'font_name']:
                        #Set indicator if word is part of chapter label
                        data.loc[row.Index, 'subchapter'] = 'subchapter'

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
                        data.loc[row.Index:row.Index+(i), 'subchapter'] = 'subchapter'

    return data



def chemicals_identifier (data):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to chem dict file
    chemicals_dir = 'data/4_chemicals/'

    #full path to chem dict file
    chempath = os.path.join(ospath, chemicals_dir)

    with open(chempath + 'cas_chemical_mapping.csv') as f:
        next(f)  # Skip the header
        reader = csv.reader(f, skipinitialspace=True)
        cas_mapping = dict(reader)
    
    #print(cas_mapping)

    data['chem'] = np.nan
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
            data.loc[row.Index, 'chem'] = int(str(31) + str(i))

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
                    data.loc[row.Index+k, 'chem'] = int(str(32) + str(i))
                # if not: check if substrings of token with len of 3 occur in cas_name
                elif len(token_down) > 3:
                    sliding_tokens = [token_down[i:i+4] for i in range(len(token_down)-3)]
                    if any(token in cas_name.lower() for token in sliding_tokens):
                        data.loc[row.Index+k, 'chem'] = int(str(32) + str(i))

                # if token is substring of cas_name --> label as name (only if len >2 or digit)
                if token_up in cas_name.lower() and len(token_up) > 2:
                    data.loc[row.Index-k, 'chem'] = int(str(32) + str(i))
                # if not: check if substrings of token with len of 3 occur in cas_name
                elif len(token_up) > 3:
                    sliding_tokens = [token_up[i:i+4] for i in range(len(token_up)-3)]
                    if any(token in cas_name.lower() for token in sliding_tokens):
                        data.loc[row.Index-k, 'chem'] = int(str(32) + str(i))

            #look for % and ranges in both directions
            j = 0

            while True:
                j += 1

                #sd 47, 57, 61, 82, 98

                if j == 100:
                    break
                
                if data.loc[row.Index-2,'word'] == '-':
                    data.loc[row.Index -3:row.Index -1 ,'chem'] = int(str(33) + str(i))
                    break

                if data.loc[row.Index+2,'word'] == '-':
                    #print(row.Index)
                    data.loc[row.Index +1:row.Index + 3 ,'chem'] = int(str(33) + str(i))
                    break

                if data.loc[row.Index+1,'word'] == '%':
                    data.loc[row.Index + 3, 'chem'] = int(str(33) + str(i))
                    break

                if data.loc[row.Index+j,'word'] == '<':
                    data.loc[row.Index +j:row.Index +j + 1, 'chem'] = int(str(33) + str(i))
                    break

                #look for % ratio around CAS number
                if data.loc[row.Index-j,'word'] == '%':
                    data.loc[row.Index -j, 'chem'] = int(str(33) + str(i))

                    #Look for all the digits assigned to the % symbol
                    t = 0
                    while True:
                        t += 1
                        # stop if '<'
                        if data.loc[row.Index -j -t, 'word'] == '<' or '≤':
                            # if <, check if token before '-' --> also range --> take token before as well
                            if data.loc[row.Index -j -t - 1, 'word'] == '-':
                                data.loc[row.Index - j - t - 2:row.Index-j, 'chem'] = int(str(33) + str(i))
                            else:
                                data.loc[row.Index - j - t:row.Index-j, 'chem'] = int(str(33) + str(i))
                            break
                        # i '-' found: range --> label until one token before '-'
                        if data.loc[row.Index -j -t, 'word'] == '-':
                            data.loc[row.Index - j - (t+1):row.Index-j, 'chem'] = int(str(33) + str(i))
                            break
                        #stop is looking for more than 10 tokens
                        if t == 10:
                            data.loc[row.Index -j -1, 'chem'] = int(str(33) + str(i))
                            break
                    break

                if data.loc[row.Index+j,'word'] == '%':
                    data.loc[row.Index +j, 'chem'] = int(str(33) + str(i))

                    #Look for all the digits assigned to the % symbol
                    t = 1 
                    while True:
                        # if '<' 
                        if data.loc[row.Index +j -t, 'word'] == '<' or '≤':
                            # if <, check if token before '-' --> also range --> take token before as well
                            if data.loc[row.Index +j -t - 1, 'word'] == '-':
                                data.loc[row.Index + j - t - 2:row.Index+j, 'chem'] = int(str(33) + str(i))
                            else:
                                data.loc[row.Index + j - t:row.Index+j, 'chem'] = int(str(33) + str(i))
                            break
                        # i '-' found: range --> label until one token before '-'
                        if data.loc[row.Index +j -t, 'word'] == '-':
                            data.loc[row.Index + j - (t+1):row.Index-j, 'chem'] = int(str(33) + str(i))
                            break

                        #stop is looking for more than 10 tokens
                        if t == 10:
                            data.loc[row.Index +j -1, 'chem'] = int(str(33) + str(i))
                            break
                        t += 1
                    break
            i += 1

    return data


def company_identifier (data):
    #Labels
    legal_forms = ['gmbh', 'ug', 'ag', 'gbr', 'e.k.', 'ohg', 'ohg', 'kg', 'se', 'lp', 'llp', 'llp', 'lllp', 'llc', 'lc', 'ltd. co', 'pllc', 'corp.', 'inc.', 'corp', 'inc', 'kluthe', 's.l.', 'bvba']
    stop_list = ['firmenname', 'firmenbezeichnung','lieferanschrift', 'lieferant', 'der', ':', ')', 'zum', 'hersteller', 'inverkehrsbringer', '*', 'firma']
    exclusion_list = ['vergiftungsinformationszentrale', 'tüv', 'website', 'gbk', '@', 'www']

    #Add new column for company name
    data['company_name'] = np.nan
    #Add new colum for status if word is part of company name
    data['company'] = np.nan

    #Loop through all rows in data
    for row in data.loc[data['Page'] <= 2, ['word_low']].itertuples(index=True):
        #search for legal form
        for lf in legal_forms:
            if lf in row.word_low:
                #start from here building string
                company_str = row.word_low
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
                        if stp in data.loc[row.Index-i,'word_low']:
                            stop_word = True
                            #break from inner stp loop
                            break
                    #check exclusion list
                    for el in exclusion_list: 
                        if (data.loc[row.Index-i,'word_low'].find(el) != -1) or (company_str.find(el) != -1):
                            excluded_str = True
                            #break from inner el loop
                            break
                    
                    #break from outer while loop
                    if stop_word == True:
                        break
                    #Add word to string
                    company_str += ' ' + data.loc[row.Index-i,'word_low']
                
                if excluded_str == False:
                    #Reverse order of strings
                    company_str_r = ' '.join(company_str.split(" ")[-1::-1])
                    #Set value for extracted company name
                    data.loc[row.Index-i+1:row.Index, 'company_name'] = company_str_r
                    #Set indicator if word is part of company name
                    data.loc[row.Index-i+1:row.Index+1, 'company'] = 'company'
            #break from outer lf loop        
            break
    return data


def date_identifier (data):
    #Labels
    date_labels = {
        #1. Druckdatum/Erstellung
        'printdate':  ['druck', 'ausgabe', 'ausstellung', 'erstellung', 'sd-datum', 'erstellt', 'ausgestellt'],
        #2. Überarbeitungsdatum
        'revisiondate':  ['überarbeit', 'änderung', 'revision', 'bearbeitung', 'quick-fds'],
        #3. Datum alte Version
        'oldversiondate':  ['ersetzt', 'ersatz', 'fassung', 'letzten'],
        #4. Gültigkeitsdatum
        'validdate':  ['kraft', 'freigabe'],
        #5. Negative Exceptions
        np.nan: ['sblcore', 'artikel']
        #6. All other not explicit listed cases are also printdate
    }

    #Add new columns for feature generation
    data['date_nr'] = np.nan
    data['date_string'] = np.nan
    data['date'] = np.nan
    data['date_stopword'] = np.nan

    #Filter out special characters for simpler trigger detection
    # & (data['Page'] == 1)
    data_iter = pd.DataFrame(data.loc[(data['special_char'] <1) & (data['Page'] == 1)])
    #Update work index + save old index
    data_iter.reset_index(inplace=True)


    #Iterrate through dataframe
    for row in data_iter.itertuples(index=True):
        
        # Catch exception with subchapter numbers
        if row.word_low.endswith('.0'):
            continue
        for fmt in (#all short/long  combinations with dot format
                    '%d.%m.%Y', '%d.%m.%y', '%w.%m.%Y', '%w.%m.%y', '%d.%-m.%Y', '%d.%-m.%y','%w.%-m.%Y','%w.%-m.%y', 
                    '%Y.%m.%d', '%y.%m.%d', '%Y.%m.%w', '%y.%m.%w', '%Y.%-m.%d', '%y.%-m.%d','%Y.%-m.%w','%y.%-m.%w',
                    #all short/long  combinations with hyphen format
                    '%d-%m-%Y', '%d-%m-%y', '%w-%m-%Y', '%w-%m-%y', '%d-%-m-%Y', '%d-%-m-%y','%w-%-m-%Y','%w-%-m-%y', 
                    '%Y-%m-%d', '%y-%m-%d', '%Y-%m-%w', '%y-%m-%w', '%Y-%-m-%d', '%y-%-m-%d','%Y-%-m-%w','%y-%-m-%w',
                    #all short/long  combinations with slash format
                    '%d/%m/%Y', '%d/%m/%y', '%w/%m/%Y', '%w/%m/%y', '%d/%-m/%Y', '%d/%-m/%y','%w/%-m/%Y','%w/%-m/%y',
                    '%Y/%m/%d', '%y/%m/%d', '%Y/%m/%w', '%y/%m/%w', '%Y/%-m/%d', '%y/%-m/%d','%Y/%-m/%w','%y/%-m/%w',
                    #all integer/text combinations 
                    '%d. %b %y', '%d %b %y', '%d. %B %y', '%d %B %y', '%w. %b %y', '%w %b %y', '%w. %B %y', '%w %B %y'
                    ):
            try:
                s = str(row.word_low)
                
                #Try to parse string in date
                date = datetime.strptime(s, fmt).date()

                #Prevent picking wrong dates
                if date < date.today():
                    org_index = int(data_iter.loc[row.Index, 'index'])
                    data.loc[org_index, 'date_nr'] = date
                    #Catch 5 words before date
                    date_str = ''
                    for i in range(5,0,-1): 
                        date_str += data_iter.loc[row.Index-i, 'word_low'] + ' '
                    data.loc[org_index, 'date_string'] = date_str

                    #search in string for label key words
                    temp = []
                    for key, value in date_labels.items ():
                        for i in value:
                            temp.append((key, date_str.find(i)))
                    #if substring was found value is >= 0
                    if max(temp, key=itemgetter(1))[1] >= 0:
                        date_label = max(temp, key=itemgetter(1))[0]

                    else:
                        date_label = 'printdate'
                    # create label in working csv
                    data.loc[org_index, 'date'] = date_label

                    # Add stopword label
                    stop = False
                    for i in range (1,6):
                        if stop == True:
                            break
                        for key, value in date_labels.items ():
                                for j in value:
                                    if data_iter.loc[row.Index-i, 'word_low'].find(j) != -1:
                                        data.loc[int(data_iter.loc[row.Index-i, 'index']),'date_stopword'] = key
                                        stop = True
                break

            except (ValueError, TypeError) as e:
                continue

    return data


def directive_identifier (data):
    #Labels
    reach_id = ['1907/2006', '2015/830']

    #Add new colum for reach status
    data['directive'] = np.nan


    #Loop through all rows in data
    for row in data.loc[data['Page'] <= 2, ['word_low']].itertuples(index=True):
        #search for reach_id
        for rid in reach_id:
            if row.word_low.find(rid) != -1:
                data.loc[row.Index, 'directive'] = 'directive'

    return data


def signal_identifier (data):
    #Labels
    reach_id = ['signalwort']
    reach_range = ['achtung', 'warnung', 'gefahr'] #,'entfällt'


    #Add new colum for reach status
    data['signal'] = np.nan

    #Filter out special characters for simpler trigger detection
    data_iter = pd.DataFrame(data.loc[data['special_char'] <1])
    #Update work index + save old index
    data_iter.reset_index(inplace=True)

    #Loop through all rows in data
    for row in data_iter.itertuples(index=True):
        #search for reach_id
        for rid in reach_id:
            if row.word_low.find(rid) != -1:
                i = 0
                keepsearching = True
                while keepsearching:
                    i +=1
                    signal = data_iter.loc[row.Index+i, 'word_low']
                    for rng in reach_range:
                        if rng == signal:
                            temp = int(data_iter.loc[row.Index+i, 'index'])
                            data.loc[temp, 'signal'] = 'signal'
                            keepsearching = False
    return data


def usecase_identifier (data):
    # Detects start and end of the whole usecase part
    usecase_start = ['abgeraten wird']
    usecase_stop = ['einzelheiten zum', 
                    '1.3. angaben',
                    '1.3 angaben',
                    'angaben des',
                    '1.3 hersteller',
                    '1.3 nationaler'
                    ]

    # Detects the starting points within the usecasepart of pro usecases (=1) and con usecases (=0)
    trigger_start = [
                    ('empfohlene r verwendungszweck e', 1),
                    ('empfohlene verwendung', 1),
                    ('verwendungen des stoffs oder gemischs', 1),
                    ('verwendung des stoffes des gemischs',1),
                    ('verwendung des stoffs des gemischs', 1),
                    ('verwendung des stoffes oder des gemisches', 1), 
                    ('verwendung des stoffs oder des gemischs', 1),
                    ('verwendung des stoffes oder gemisches', 1), 
                    ('verwendung des stoffs oder gemischs', 1),
                    ('verwendung des stoffes des gemisches', 1), 
                    ('verwendung des stoffs des gemischs',1),
                    ('identifizierte verwendungen', 1),
                    ('identifizierte anwendungen', 1),
                    #('funktions- oder verwendungskategorie', 1),
                    ('relevante verwendungen', 1),
                    #('verwendungssektor', 1),
                    ('bestimmte verwendung der mischung',1),
                    ('vorgesehene verwendung', 1),
                    ('nicht empfohlene verwendung der mischung', 0),
                    ('verwendungen von denen abgeraten wird', 0),
                    ('nicht vorgesehene verwendung', 0),
                    ('abgeratene verwendungen', 0),
                    ('abgeratene anwendungen', 0)
                    ]
    # Detects the ending points within the usecasepart of pro usecases (=1) and con usecases (=0) // Note: new usecase introduction could be endingpoint of previous usecase section

    '''             'empfohlene r verwendungszweck e',
                    'empfohlene verwendung',
                    'verwendungen des stoffs oder gemischs',
                    'verwendung des stoffs des gemischs',
                    'verwendung des stoffes oder des gemisches', 
                    'verwendung des stoffs oder des gemischs',
                    'verwendung des stoffes oder gemisches', 
                    'verwendung des stoffs oder gemischs',
                    'verwendung des stoffes des gemisches', 
                    'verwendung des stoffs des gemischs',
                    'identifizierte verwendungen',
                    'identifizierte anwendungen',
                    'funktions- oder verwendungskategorie',
                    'relevante verwendungen',
                    'verwendungssektor',  '''

    trigger_end = [
                    #'verwendungssektor',
                    'nicht empfohlene verwendung der mischung',
                    'verwendungen von denen abgeraten wird',
                    'vorgesehene verwendung',
                    'abgeratene verwendungen',
                    'abgeratene anwendung',

                    #'produktkategorie', 
                    #'kontaktieren sie ihren lieferanten für weitere informationen',
                    #'es sind keine verwendungen bekannt',
                    #'zur zeit liegen keine Informationen hierzu vor',
                    'wirkung des stoffes',
                    #'keine weitere information vorhanden', 
                    #'keine weitere information vorhanden',
                    #'keine weiteren relevanten informationen verfügbar',
                    #'keine bekannt',
                    #'bestimmt für die allgemeinheit',
                    #'hauptverwendungskategorie',
                    #'zur zeit',
                    '1.2.2',
                    '1.3',
                    'einzelheiten zum',
                    'angaben des lieferanten',
                    ]

    #Add new column for part string
    data['usecase_part'] = np.nan
    #Add new column for usecase
    data['usecase'] = np.nan



    #Filter out special characters for simpler trigger detection
    data_iter = pd.DataFrame(data.loc[data['special_char'] <1])
    #Update work index + save old index
    data_iter.reset_index(inplace=True)

    #start with index 1 because of sliding window (range = 2)
    index = 1

    length = len(data_iter['index'])-1

    while index < length:
        
        row = data_iter.loc[index, :]

        yo = row.doc

        # Sliding window of start point
        start_str = data_iter.loc[index-1, 'word_low'] + ' ' + row.word_low

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
                    stop_str = data_iter.loc[i+1,'word_low'] + ' ' + data_iter.loc[i+2,'word_low']
                    for stop in usecase_stop:
                        if stop in stop_str:
                            recording=False
                    if recording == False:
                        break
                    usecase_str = usecase_str + ' ' + data_iter.loc[i, 'word_low']
                # search corresponding index of unfiltered dataframe
                temp1 = int(data_iter.loc[i, 'index'])
                temp4 = int(data_iter.loc[index, 'index'])
                # add usecase string with the whole part to last index of part
                data.loc[temp4+1:temp1, 'usecase_part'] = usecase_str
                
                
                #start searching for usecases from this position
                detect_start = ''
                keepsearching = True
                end_index = 0
                #j = index+1
                j = index
                while j < i:
                    keepsearching = True
                    # build string
                    detect_start = detect_start + ' ' + data_iter.loc[j, 'word_low']
                    j +=1
                    for trig_st in trigger_start:
                        #if trigger was found start searching for the end of this (sub-)part
                        if detect_start.find(trig_st[0]) != -1:
                            detect_end = ''
                            k = j
                            while keepsearching:
                                k +=1
                                detect_end = detect_end + ' ' + data_iter.loc[k, 'word_low']

                                for trig_en in trigger_end:
                                    # if end trigger was found retunr last index of part
                                    if detect_end.find(trig_en) != -1:
                                        # last index of part is overall number of words in the string minus the length of the trigger
                                        end_index = k-len(trig_en.split())
                                        # convert the found range in the range of the unprocessed dataframe
                                        temp2 = int(data_iter.loc[j, 'index'])
                                        temp3 = int(data_iter.loc[end_index, 'index'])
                                        # check if part is pro or con usecase
                                        if trig_st[1] == 1:
                                            helpcheck = data_iter.loc[j, 'word_low'] + ' ' + data_iter.loc[j+1, 'word_low']
                                            if helpcheck == 'des stoffs':
                                                temp2 = int(data_iter.loc[j+4, 'index'])
                                                data.loc[temp2:temp3, 'usecase'] = 'usecase_pro'
                                            else:
                                                data.loc[temp2:temp3, 'usecase'] = 'usecase_con'
                                        else:
                                            data.loc[temp2:temp3, 'usecase'] = 'usecase_con'
                                        j = end_index
                                        keepsearching = False
                                        detect_start = ''
                                        break
                            break
                    #j +=1
                
                index = j
            break
        index +=1

    return data


def version_identifier (data):
    #get list of all words
    words = list(data['word'])

    version_dict = {
        'Versionsnummer', 'Version', 'Versionsnummer:' , 'Version:' , 'Revisions-Nr:' , 'Revisions-Nr',
        'Revisions-nr' , 'Revisionsnummer' , 'Revisionsnummer:', 'Rev-Nr:' , 'Version-Nr'
    }

    l1 = []

    for c in version_dict:

        for i, e in enumerate(words):       
            if words[i-1] == c:
                if words[i] == '(': # Versionsnummer und in Klammern alte Versionsnummer
                    l1.append(i+4)
                elif words[i] == ':': # wenn zwischen Version und : Leerzeichen vorkommmt -> naechstes 
                    if words[i-4]== 'Überarbeitet':
                        l1.append(i+3)
                    elif words[i-5] != 'Ersetzt' and words[i-3] != 'Ersetzt':
                        l1.append(i+1)
                elif words[i] == '.': 
                    l1.append(i+2)
                else:
                    l1.append(i)
                
    # fill in identified labels in data
    data['version'] = np.nan
    for j in l1:
        data.loc[j,'version'] = 'version'

    return data


def combine_labels (data):
    
    labels = [
                'chapter',
                'subchapter',
                'date',
                'version',
                'directive',
                'signal',
                'usecase',
                'chem',
                'company'          
    ]
    
    #data['label'] = np.nan
    data['label'] = ''

    for l in labels:
        data["label"] = data["label"] + data.loc[:, l].astype(str).replace('nan', '')
    
    #for l in labels:
        #data['label'] = data['label'].str.cat(data[l])


    '''
    for row in data.loc[:, ['label']].itertuples(index=True):
        for label in labels:
            temp = data.loc[row.Index, label]
            if pd.isna (temp) == False:
                data.loc[row.Index, 'label'] = temp
                break
    '''
        
    '''
    data['label'] = np.nan
    
    data['nr_labels'] = np.nan

    data['nr_labels'] = data[labels].apply(lambda x: x.notnull().sum(), axis='columns')

    data['label'] = data[labels].max(1) 
    
    #data = data.drop(labels, 1)
    '''
    
    return data

def main ():
    
    data = prepare_data('data_all_avg_ordered.csv')
    
    #Select identifiers to run
    identifier = [
        chap_identifier,           
        subchapter_identifier,     
        date_identifier,
        version_identifier,         
        directive_identifier,      
        signal_identifier,         
        usecase_identifier,             
        chemicals_identifier,
        company_identifier       
        ]
    
    for i in identifier:
        print ('********** Start: ' + i.__name__ + ' **********')
    
        data = i (data)

        print ('********** End: ' + i.__name__ + ' **********')
    
    combine_labels(data)
    
    create_output(data, 'data_all_labeled.csv')

    
if __name__ == '__main__':
    main()
