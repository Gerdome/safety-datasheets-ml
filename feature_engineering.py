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

def delete_samples (data):
    
    wrong = ['008_sd.pdf', '029_sd.pdf', '035_sd.pdf', '041_sd.pdf', '043_sd.pdf', '045_sd.pdf', '049_sd.pdf', '050_sd.pdf', '051_sd.pdf', '052_sd.pdf', '053_sd.pdf', '055_sd.pdf', '056_sd.pdf', '059_sd.pdf', '061_sd.pdf', '062_sd.pdf', '064_sd.pdf', '077_sd.pdf', '081_sd.pdf', '089_sd.pdf', '091_sd.pdf', '093_sd.pdf', '096_sd.pdf', '105_sd.pdf', '106_sd.pdf', '108_sd.pdf', '115_sd.pdf', '116_sd.pdf', '117_sd.pdf', '118_sd.pdf', '120_sd.pdf', '121_sd.pdf', '122_sd.pdf', '123_sd.pdf', '144_sd.pdf', '164_sd.pdf', '165_sd.pdf', '169_sd.pdf', '170_sd.pdf', '175_sd.pdf', '176_sd.pdf', '177_sd.pdf', '180_sd.pdf', '181_sd.pdf', '182_sd.pdf', '183_sd.pdf', '184_sd.pdf', '185_sd.pdf', '186_sd.pdf', '187_sd.pdf', '188_sd.pdf', '191_sd.pdf', '193_sd.pdf', '194_sd.pdf', '195_sd.pdf', '198_sd.pdf', '199_sd.pdf', '200_sd.pdf', '201_sd.pdf', '205_sd.pdf', '208_sd.pdf', '212_sd.pdf', '213_sd.pdf', '214_sd.pdf', '215_sd.pdf', '216_sd.pdf', '217_sd.pdf', '226_sd.pdf', '248_sd.pdf', '249_sd.pdf', '260_sd.pdf', '268_sd.pdf', '269_sd.pdf', '270_sd.pdf', '271_sd.pdf', '277_sd.pdf', '278_sd.pdf', '279_sd.pdf', '280_sd.pdf', '281_sd.pdf', '285_sd.pdf', '321_sd.pdf', '322_sd.pdf', '323_sd.pdf', '332_sd.pdf', '337_sd.pdf', '338_sd.pdf', '340_sd.pdf', '341_sd.pdf', '344_sd.pdf', '345_sd.pdf', '346_sd.pdf', '347_sd.pdf', '353_sd.pdf', '354_sd.pdf', '357_sd.pdf', '358_sd.pdf', '359_sd.pdf', '361_sd.pdf', '362_sd.pdf', '363_sd.pdf', '364_sd.pdf', '371_sd.pdf', '374_sd.pdf', '375_sd.pdf', '376_sd.pdf', '377_sd.pdf', '378_sd.pdf', '380_sd.pdf', '381_sd.pdf', '383_sd.pdf', '384_sd.pdf', '385_sd.pdf', '386_sd.pdf', '392_sd.pdf', '402_sd.pdf', '403_sd.pdf', '408_sd.pdf', '409_sd.pdf', '410_sd.pdf', '423_sd.pdf', '424_sd.pdf', '425_sd.pdf', '430_sd.pdf', '455_sd.pdf', '456_sd.pdf', '457_sd.pdf', '458_sd.pdf', '462_sd.pdf', '463_sd.pdf', '464_sd.pdf', '465_sd.pdf', '466_sd.pdf', '467_sd.pdf', '468_sd.pdf', '469_sd.pdf', '479_sd.pdf', '528_sd.pdf', '530_sd.pdf', '531_sd.pdf', '532_sd.pdf', '533_sd.pdf', '534_sd.pdf', '535_sd.pdf', '536_sd.pdf', '537_sd.pdf', '538_sd.pdf', '539_sd.pdf', '540_sd.pdf', '542_sd.pdf', '543_sd.pdf', '544_sd.pdf', '545_sd.pdf', '546_sd.pdf', '547_sd.pdf', '548_sd.pdf', '549_sd.pdf', '550_sd.pdf', '559_sd.pdf', '560_sd.pdf', '562_sd.pdf', '563_sd.pdf', '564_sd.pdf', '565_sd.pdf', '566_sd.pdf', '567_sd.pdf', '583_sd.pdf', '602_sd.pdf', '603_sd.pdf', '644_sd.pdf', '677_sd.PDF', '715_sd.pdf', '721_sd.pdf', '724_sd.pdf', '731_sd.pdf']

    filtered = data[~data.doc.isin(wrong)]
    filtered = filtered[pd.notnull(filtered['doc'])]
    filtered = filtered.reset_index(drop=True)

    return filtered


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