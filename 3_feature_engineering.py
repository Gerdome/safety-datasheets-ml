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
import pickle
from gensim.models import KeyedVectors

def prepare_data (filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #path for demo purposes (only 3 PDFs)
    demodir = 'data/demo/'

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files - !! Change demodir to datadir for running with all PDFs !!
    datapath = os.path.join(ospath, demodir)

    dtype={'user_id': int}

    #read raw data csv
    data = pd.read_csv(datapath + filename, encoding='utf-8-sig', index_col=0)

    return data

def create_output (data, filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #path for demo purposes (only 3 PDFs)
    demodir = 'data/demo/'

    #full path to data files - !! Change demodir to datadir for running with all PDFs !!
    datapath = os.path.join(ospath, demodir)  

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

    orientation_col = data[['doc', 'Page', 'word', 'label']]

    labels = data.loc[:,'chapter':'company']

    final_data = pd.concat((orientation_col, labels,features, data[['ycord_average', 'Xcord_first']]), axis=1, sort=False)
        
    return final_data

def create_window (data):
    
    #Feature Groups
    ort_col = ['doc', 'Page', 'word', 'label', 'label_dum']
    labels = ['chapter', 'subchapter', 'version', 'directive', 'signal', 'chem', 'company', 'date', 'date_oldversiondate', 'date_printdate', 'date_revisiondate', 'date_validdate', 'usecase', 'usecase_con', 'usecase_pro']
    paper_feature = ['word.is.lower', 'word.is.upper', 'word.is.mixed.case', 'word.is.digit', 'word.contains.digit', 'word.is.special.char','word.len.1', 'word.len.3', 'word.len.5', 'word.len.7', 'word.len.9', 'word.len.11', 'word.len.13', 'word.is.stop']
    date_specific_feature = ['word.is.print.date.trigger', 'word.is.revision.date.trigger', 'word.is.valid.date.trigger', 'word.is.oldversion.date.trigger']
    #dropped 'word.contains.special.char'
    new_feature = ['word.is.title', 'word.is.bold', 'word.is.newline','ycord_average','Xcord_first', 'grid.area_11', 'grid.area_12', 'grid.area_13', 'grid.area_14', 'grid.area_15', 'grid.area_16', 'grid.area_17', 'grid.area_18', 'grid.area_21', 'grid.area_22', 'grid.area_23', 'grid.area_24', 'grid.area_25', 'grid.area_26', 'grid.area_27', 'grid.area_28', 'grid.area_31', 'grid.area_32', 'grid.area_33', 'grid.area_34', 'grid.area_35', 'grid.area_36', 'grid.area_37', 'grid.area_38', 'grid.area_41', 'grid.area_42', 'grid.area_43', 'grid.area_44', 'grid.area_45', 'grid.area_46', 'grid.area_47', 'grid.area_48', 'is.page.1', 'is.page.2', 'is.page.3']

    data_ord = data[ort_col + labels]

    columns = [paper_feature, date_specific_feature, new_feature]

    #create window for all features except word embedding
    window_size_feat = 13
    #copies the previous and following features for every token in a given window
    for col in range (len(columns)):
        sel_col = data[columns[col]]
        data_ord = pd.concat([data_ord, sel_col], axis=1, sort=False)
        for i in range (1, math.ceil(window_size_feat/2)):
            print ('Window: ',col,i)
            data_pre = sel_col.shift(i).add_prefix ('-' + str(i) + '_')
            data_suc = sel_col.shift(-i).add_prefix ('+' + str(i) + '_')
            data_ord = pd.concat([data_ord, data_pre, data_suc], axis=1, sort=False)
    
    data_ord.to_pickle('data_model_allfeatw13.pkl')

    #create window for word embedding
    window_size_emb = 13
    sel_col = data.loc[:,'0':'299']
    data_ord = pd.concat([data_ord, sel_col], axis=1, sort=False)
    for i in range (1, math.ceil(window_size_emb/2)):
        print ('Window_Emb: ',i)
        data_pre = sel_col.shift(i).add_prefix ('-' + str(i) + '_')
        data_suc = sel_col.shift(-i).add_prefix ('+' + str(i) + '_')
        data_ord = pd.concat([data_ord, data_pre, data_suc], axis=1, sort=False)
        data_ord.to_pickle('data_model_allfeatw13_web' + str(i) + '.pkl')

    return data_ord


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
    
    label_dum = pd.DataFrame(data['label'])
    label_dum = pd.DataFrame(label_dum.loc[:,'label'].astype('category').cat.codes)
    data.insert(loc=5, column = 'label_dum', value = label_dum)

    #first columns as id, not part of the model 
    orientation_col = data.loc[:, 'doc':'label_dum']
    
    #select feature columns
    features = data.loc[:, 'word.is.lower':'Xcord_first']
    #change remaining features from True/False to 0/1
    features.loc[:,'word.is.lower'] = features['word.is.lower'].astype(int)
    features.loc[:,'word.is.title'] = features['word.is.title'].astype(int)
    features.loc[:,'word.is.upper'] = features['word.is.upper'].astype(int)
    features.loc[:,'word.is.digit'] = features['word.is.digit'].astype(int)

    

    encoded_data = pd.concat((orientation_col, labels_dummies, date_dummies, usecase_dummies, features), axis=1, sort=False)

    return encoded_data

def create_word_embedding (data):
    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #load existing embeddings
    print ('Start: Vectors loading')
    en_model = KeyedVectors.load_word2vec_format(os.path.join(ospath, 'data/4_Word2Vec/cc.de.300.vec'))


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
    
    data = prepare_data('02_data.csv')

   #data =  pd.read_pickle('./data_model_wordembedding.pkl')

    #Select identifiers to run
    methods = [         
        create_features,
        encode_columns,     
        #create_word_embedding,
        create_window,         
        ]
    
    for i in methods:
        print ('********** Start: ' + i.__name__ + ' **********')
    
        data = i (data)

        print ('********** End: ' + i.__name__ + ' **********')

    #data.to_pickle('./data_model_window13.pkl')

    create_output(data, '03_data.csv')
    
if __name__ == '__main__':
    main()