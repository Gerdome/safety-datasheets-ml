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
import math
import pickle
from gensim.models import KeyedVectors

def prepare_data (filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files
    datapath = os.path.join(ospath, datadir)

    dtype={'user_id': int}

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
            features['word.is.mixed.case'].append(1)
        else:
            features['word.is.mixed.case'].append(0)

        if 'bold' in str(data.loc[i,'font_name']).lower():
            features['word.is.bold'].append(1)
        else:
            features['word.is.bold'].append(0)


        '''
        meta information: type of characters
        '''

        features['word.is.digit'].append(str(w).isdigit())
        if any(x.isdigit() for x in str(w)):
            features['word.contains.digit'].append(1)
        else:
            features['word.contains.digit'].append(0)

        if str(w) in special_chars:
            features['word.is.special.char'].append(1)
        else:
            features['word.is.special.char'].append(0)
        if any(x in str(w) for x in special_chars):
            features['word.contains.special.char'].append(1)
        else:
            features['word.contains.special.char'].append(0)

    
        '''
        length of words
        '''
        if len(str(w)) > 12:
            features['word.len.13'].append(1)
            for l in (1,3,5,7,9,11):
                features['word.len.' + str(l)].append(0)
        elif len(str(w)) > 10:
            features['word.len.11'].append(1)
            for l in (1,3,5,7,9,13):
                features['word.len.' + str(l)].append(0)
        elif len(str(w)) > 8:
            features['word.len.9'].append(1)
            for l in (1,3,5,7,11,13):
                features['word.len.' + str(l)].append(0)
        elif len(str(w)) > 6:
            features['word.len.7'].append(1)
            for l in (1,3,5,9,11,13):
                features['word.len.' + str(l)].append(0)
        elif len(str(w)) > 4:
            features['word.len.5'].append(1)
            for l in (1,3,7,9,11,13):
                features['word.len.' + str(l)].append(0)
        elif len(str(w)) > 2:
            features['word.len.3'].append(1)
            for l in (1,5,7,9,11,13):
                features['word.len.' + str(l)].append(0)
        else:
            features['word.len.1'].append(1)
            for l in (3,5,7,9,11,13):
                features['word.len.' + str(l)].append(0)

        '''
        Semantic
        '''



        if str(w) in stopWords:
            features['word.is.stop'].append(1)
        else:
            features['word.is.stop'].append(0)

        if str(w).lower() in ['druck', 'ausgabe', 'ausstellung', 'erstellung', 'sd-datum', 'erstellt', 'ausgestellt']:
            features['word.is.print.date.trigger'].append(1)
        else:
            features['word.is.print.date.trigger'].append(0)
        
        if str(w).lower() in ['überarbeit', 'änderung', 'revision', 'bearbeitung', 'quick-fds']:
            features['word.is.revision.date.trigger'].append(1)
        else:
            features['word.is.revision.date.trigger'].append(0)

        if str(w).lower() in  ['ersetzt', 'ersatz', 'fassung', 'letzten']:
            features['word.is.oldversion.date.trigger'].append(1)
        else:
            features['word.is.oldversion.date.trigger'].append(0)

        if str(w).lower() in ['kraft', 'freigabe']:
            features['word.is.valid.date.trigger'].append(1)
        else:
            features['word.is.valid.date.trigger'].append(0)


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
            features['is.page.1'].append(1)
            features['is.page.2'].append(0)
            features['is.page.3'].append(0)
        elif data.loc[i,'Page'] == 2:
            features['is.page.1'].append(0)
            features['is.page.2'].append(1)
            features['is.page.3'].append(0)
        elif data.loc[i,'Page'] == 3:
            features['is.page.1'].append(0)
            features['is.page.2'].append(0)
            features['is.page.3'].append(1)

        if i > 1:
            if data.loc[i,'ycord_average'] != data.loc[i-1,'ycord_average']:
                features['word.is.newline'].append(1)
            else:
                features['word.is.newline'].append(0)
        else:
            features['word.is.newline'].append(1)

    #for f in features:
        #print(len(features[f]))
            
    features = pd.DataFrame(features)

    orientation_col = data[['doc', 'Page', 'ycord_average', 'word', 'label']]

    labels = data.loc[:,'chapter':'company']

    final_data = pd.concat((orientation_col, labels,features), axis=1, sort=False)
        
    return final_data

def create_window (data):
    #set window size
    window_size = 13

    #make embedding columns selectable as string for loc
    data.columns = data.columns.astype(str)

    final_data = pd.DataFrame (data)

    #copies the previous and following features for every token in a given window
    for i in range (1, math.ceil(window_size/2)):
        print ('Window: ',i)
        data_pre = data.loc[:, 'word.is.lower':'299'].shift(i).add_prefix ('-' + str(i) + '_')
        data_suc = data.loc[:, 'word.is.lower':'299'].shift(-i).add_prefix ('+' + str(i) + '_')
        final_data = pd.concat([final_data, data_pre, data_suc], axis=1, sort=False)
    
    return final_data


def encode_columns (data): 
    
    #one-hot encode lables with multiclass
    data.loc [:,'date'] = pd.Categorical(data['date'])
    date_dummies = pd.get_dummies(data['date'], prefix = 'date') 
    data.loc [:,'usecase'] = pd.Categorical(data['usecase'])
    usecase_dummies = pd.get_dummies(data['usecase'])
    data.loc [:,'grid.area'] = pd.Categorical(data['grid.area'])
    date_dummies = pd.get_dummies(data['grid.area'], prefix = 'grid.area') 

    #drop features which are not used in the modell
    data = data.drop(['date_nr', 'date_string', 'date_stopword', 'chapter 3.2', 'company_name', 'usecase_part'], 1)   

    #encode labels with one class
    labels_dummies = pd.DataFrame(data.loc[:,'chapter':'company'])
    for cl in labels_dummies.columns:
        labels_dummies[cl] = labels_dummies[cl].astype ('category').cat.codes
        #first value != nan gets 0 --> change to 1
        labels_dummies[cl] = labels_dummies[cl].replace(0, 1)
        #nan values get to -1 by catcodes --> change to 0
        labels_dummies[cl] = labels_dummies[cl].replace(-1, 0)
    
    #first columns as id, not part of the model 
    orientation_col = data.loc[:, 'doc':'label']
    
    #select feature columns
    features = data.loc[:, 'word.is.lower':'word.is.newline']
    #change remaining features from True/False to 0/1
    features.loc[:,'word.is.lower'] = features['word.is.lower'].astype(int)
    features.loc[:,'word.is.title'] = features['word.is.lower'].astype(int)
    features.loc[:,'word.is.upper'] = features['word.is.lower'].astype(int)
    features.loc[:,'word.is.digit'] = features['word.is.digit'].astype(int)

    encoded_data = pd.concat((orientation_col, labels_dummies, date_dummies, usecase_dummies, features), axis=1, sort=False)

    return encoded_data

def create_word_embedding (data):
    #load existing embeddings
    print ('Start: Vectors loading')
    en_model = KeyedVectors.load_word2vec_format('cc.de.300.vec')


    #preprocess words
    word_emb_input = pd.DataFrame(data.loc[:,'word'].str.lower())
    word_emb_input = pd.DataFrame(word_emb_input)
    word_emb_input = word_emb_input.astype(str)
    word_emb_input['preprocessed'] = np.nan
    word_emb_input ['preprocessed'] = [re.sub('\d', 'D', x) for x in word_emb_input['word'].tolist()]
    word_emb_input = word_emb_input.drop(['word'],1)
   
    #create embeddings
    print ('Start: Embedding')
    '''emb = pd.DataFrame ()
    for row in word_emb_input.loc[:, ['preprocessed']].itertuples(index=True):
        print (row.Index)
        try:
            emb =  pd.concat([emb, pd.DataFrame (en_model[row.preprocessed]).transpose()])
        except:
            emb =  pd.concat([emb, pd.DataFrame (np.full((1, 300), 0.0))])
    '''
    '''
    words = list(word_emb_input.loc[:,'preprocessed'])
    emb = np.array(np.full((1, 300), 0.0))
    nv = np.array(np.full((1, 300), 0.0))
    i = 0
    for x in words:
        print (i)
        try:
            emb = np.append (emb, np.array([en_model[x]]), axis = 0)
        except:
            emb = np.append (emb, nv, axis = 0)
        i +=1

    emb_df = pd.DataFrame(emb)
    emb_df = emb_df.iloc[1:]
    '''

    #calculate embeddings for every word
    missing=[0]*300
    def fun(key):
        try:
            return(en_model[key])
        except:
            return(missing)
    word_emb_input['vector'] = word_emb_input['preprocessed'].apply(fun)
    word_emb = pd.DataFrame(word_emb_input['vector'].values.tolist())

    #concat data
    emb_data = pd.concat((data, word_emb), axis=1, sort=False)

    return emb_data



def main ():
    
    #data = prepare_data('data_all_labeled.csv')

    data =  pd.read_pickle('./data_model_wordembedding.pkl')

    #Select identifiers to run
    methods = [         
        #create_features,
        #encode_columns,     
        #create_word_embedding,
        create_window,         
        ]
    
    for i in methods:
        print ('********** Start: ' + i.__name__ + ' **********')
    
        data = i (data)

        print ('********** End: ' + i.__name__ + ' **********')

    data.to_pickle('./data_model_window13.pkl')

    #create_output(data, 'final.csv')
    
if __name__ == '__main__':
    main()