from datetime import datetime
import pandas as pd
import numpy as np
from nltk import FreqDist
from nltk.corpus import stopwords
import os 
import re
from operator import itemgetter
import datetime
from dateutil.parser import parse
from nltk.corpus import stopwords
import math


def prepare_data (filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files
    datapath = os.path.join(ospath, datadir)

    #read raw data csv
    data = pd.read_csv(datapath + filename, encoding='utf-8-sig', index_col=0)

    return data

def create_output (data, filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files
    datapath = os.path.join(ospath, datadir)    

    data.to_csv(datapath + filename, encoding='utf-8-sig')

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(str(string), fuzzy=fuzzy)
        return True

    except ValueError:
        return False
    
    except OverflowError:
        return False

def create_features (data):

    words = list(data['word'])

    #set german stopwords
    stopWords = set(stopwords.words('german'))

    # define own special character set 
    special_chars = ('.',',','(', ')', '–', '[', '·','{', '}', ']', ':', ';', "'", '"','?', '/', '*','!', '@', '#', '&', '"*"', '`', '~', '$', '^', '+', '=', '<', '>','%')

    #prepare ranges for x-y-coordinate grid classification
    num_rows = 8
    num_cols = 4

    x_width = int(max(data['Xcord_first'])) / num_cols
    y_width = int(max(data['ycord_average'])) / num_rows


    features = {

    # meta information: style of characters

        'word.is.lower': [],
        'word.is.upper': [],
        'word.is.title': [],
        'word.is.mixed.case': [],
        'word.is.bold':[],
        

    # meta information: type of characters

        'word.is.digit': [],
        'word.contains.digit':[],
        'word.is.special.char' :[],
        'word.contains.special.char' :[],


    # length of words

        'word.len.1':[],
        'word.len.3':[],
        'word.len.5':[],
        'word.len.7':[],
        'word.len.9':[],
        'word.len.11':[],
        'word.len.13':[],

    # Semantic

        #'word.pos':[],
        'word.is.stop':[],
        'word.is.print.date.trigger':[],
        'word.is.revision.date.trigger':[],
        'word.is.oldversion.date.trigger':[],
        'word.is.valid.date.trigger':[],


        # Graphical Information / Location of word(token)
        'grid.area':[],

        'is.page.1':[],
        'is.page.2':[],
        'is.page.3':[],

        'word.is.newline': []    



        }

    '''
    # Graphical Information / Location of word(token)


        'word.is.koord.1':[],
        'word.is.koord.2':[],
        'word.is.koord.3':[],
        'word.is.koord.4':[],
        'word.is.koord.5':[],
        'word.is.koord.6':[],
        'word.is.koord.7':[],
        'word.is.koord.8':[],

        'is.page.1':[],
        'is.page.2':[],
        'is.page.3':[],

        'word.is.newline': []    
    '''


    for i, w in enumerate(words):

        '''
        meta information: style of characters
        '''
        features['word.is.lower'].append(str(w).islower())
        features['word.is.upper'].append(str(w).isupper())
        features['word.is.title'].append(str(w).istitle())

        if not str(w).islower() and not str(w).isupper():
            features['word.is.mixed.case'].append(True)
        else:
            features['word.is.mixed.case'].append(False)

        if 'bold' in str(data.loc[i,'font_name']).lower():
            features['word.is.bold'].append(True)
        else:
            features['word.is.bold'].append(False)


        '''
        meta information: type of characters
        '''

        features['word.is.digit'].append(str(w).isdigit())
        if any(x.isdigit() for x in str(w)):
            features['word.contains.digit'].append(True)
        else:
            features['word.contains.digit'].append(False)

        if str(w) in special_chars:
            features['word.is.special.char'].append(True)
        else:
            features['word.is.special.char'].append(False)
        if any(x in str(w) for x in special_chars):
            features['word.contains.special.char'].append(True)
        else:
            features['word.contains.special.char'].append(False)

    
        '''
        length of words
        '''
        if len(str(w)) > 12:
            features['word.len.13'].append(True)
            for l in (1,3,5,7,9,11):
                features['word.len.' + str(l)].append(False)
        elif len(str(w)) > 10:
            features['word.len.11'].append(True)
            for l in (1,3,5,7,9,13):
                features['word.len.' + str(l)].append(False)
        elif len(str(w)) > 8:
            features['word.len.9'].append(True)
            for l in (1,3,5,7,11,13):
                features['word.len.' + str(l)].append(False)
        elif len(str(w)) > 6:
            features['word.len.7'].append(True)
            for l in (1,3,5,9,11,13):
                features['word.len.' + str(l)].append(False)
        elif len(str(w)) > 4:
            features['word.len.5'].append(True)
            for l in (1,3,7,9,11,13):
                features['word.len.' + str(l)].append(False)
        elif len(str(w)) > 2:
            features['word.len.3'].append(True)
            for l in (1,5,7,9,11,13):
                features['word.len.' + str(l)].append(False)
        else:
            features['word.len.1'].append(True)
            for l in (3,5,7,9,11,13):
                features['word.len.' + str(l)].append(False)

        '''
        Semantic
        '''



        if str(w) in stopWords:
            features['word.is.stop'].append(True)
        else:
            features['word.is.stop'].append(False)

        if str(w).lower() in ['druck', 'ausgabe', 'ausstellung', 'erstellung', 'sd-datum', 'erstellt', 'ausgestellt']:
            features['word.is.print.date.trigger'].append(True)
        else:
            features['word.is.print.date.trigger'].append(False)
        
        if str(w).lower() in ['überarbeit', 'änderung', 'revision', 'bearbeitung', 'quick-fds']:
            features['word.is.revision.date.trigger'].append(True)
        else:
            features['word.is.revision.date.trigger'].append(False)

        if str(w).lower() in  ['ersetzt', 'ersatz', 'fassung', 'letzten']:
            features['word.is.oldversion.date.trigger'].append(True)
        else:
            features['word.is.oldversion.date.trigger'].append(False)

        if str(w).lower() in ['kraft', 'freigabe']:
            features['word.is.valid.date.trigger'].append(True)
        else:
            features['word.is.valid.date.trigger'].append(False)


        # Graphical Information / Location of word(token)

        for r in reversed(range(num_rows)):
            if data.loc[i,'ycord_average'] > r*y_width:
                y_cluster = r+1
                break
            else:
                y_cluster = 1
        for c in reversed(range(num_cols)):
            if data.loc[i,'Xcord_first'] > c*x_width:
                x_cluster = c+1
                break
            else:
                x_cluster = 1

        cluster = str(str(x_cluster) + str(y_cluster))
        features['grid.area'].append(cluster)

        if data.loc[i,'Page'] == 1:
            features['is.page.1'].append(True)
            features['is.page.2'].append(False)
            features['is.page.3'].append(False)
        elif data.loc[i,'Page'] == 2:
            features['is.page.1'].append(False)
            features['is.page.2'].append(True)
            features['is.page.3'].append(False)
        elif data.loc[i,'Page'] == 3:
            features['is.page.1'].append(False)
            features['is.page.2'].append(False)
            features['is.page.3'].append(True)

        if i > 1:
            if data.loc[i,'ycord_average'] != data.loc[i-1,'ycord_average']:
                features['word.is.newline'].append(True)
            else:
                features['word.is.newline'].append(False)
        else:
            features['word.is.newline'].append(True)




    for f in features:
        print(len(features[f]))
            
    features = pd.DataFrame(features)

    final_data = pd.concat([data, features], axis=1, sort=False)
        
    #final_data = final_data.drop(labels,1)

    return final_data

    '''

            #1. Druckdatum/Erstellung
            5:  ['druck', 'ausgabe', 'ausstellung', 'erstellung', 'sd-datum', 'erstellt', 'ausgestellt'],
            #2. Überarbeitungsdatum
            6:  ['überarbeit', 'änderung', 'revision', 'bearbeitung', 'quick-fds'],
            #3. Datum alte Version
            7:  ['ersetzt', 'ersatz', 'fassung', 'letzten'],
            #4. Gültigkeitsdatum
            8:  ['kraft', 'freigabe'],


    if i > 3:
            features['word[-1]'].append(str(words[i-1]))
            features['word[-2]'].append(str(words[i-2]))
            features['word[-3]'].append(str(words[i-3]))
            features['-1:word.lower'].append(str(words[i-1]).lower())
            features['-1:word.istitle'].append(str(words[i-1]).istitle())
            features['-1:word.isupper'].append(str(words[i-1]).isupper())

            if str(words[i-1]) in ('.',',','(', ')', '–', '[', '·','{', '}', ']', ':', ';', "'", '"','?', '/', '*','!', '@', '#', '&', '"*"', '`', '~', '$', '^', '+', '=', '<', '>','%'):
                features['-1:word.isspecial.char'].append(True)
            else:
                features['-1:word.isspecial.char'].append(False)

        else:
            features['word[-1]'].append(np.nan)
            features['word[-2]'].append(np.nan)
            features['word[-3]'].append(np.nan)
            features['-1:word.lower'].append(np.nan)
            features['-1:word.istitle'].append(np.nan)
            features['-1:word.isupper'].append(np.nan)
            features['-1:word.isspecial.char'].append(np.nan)

    '''

def create_window (data, window_size):
    
    final_data = pd.DataFrame (data)

    for i in range (1, math.ceil(window_size/2)):
        data_pre = data.loc[:, 'word.is.lower':'word.is.newline'].shift(i).add_prefix ('-' + str(i) + '_')
        data_suc = data.loc[:, 'word.is.lower':'word.is.newline'].shift(-i).add_prefix ('+' + str(i) + '_')
        final_data = pd.concat([final_data, data_pre, data_suc], axis=1, sort=False)
    
    return final_data

def main ():
    
    data = prepare_data('data_all_labeled.csv')

    #data = create_features(data)

    #data = create_window(data, 13)

    #create_output(data, 'final.csv')
    
if __name__ == '__main__':
    main()