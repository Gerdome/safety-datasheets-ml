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



#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/2_final/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'labeled_data.csv', dtype=str, encoding='utf-8-sig', index_col=0)

'''
def word2features(sent, i):
    print(i)
    word = str(sent[i])
    #postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': str(sent[i-3]),
        'word[-2:]': str(sent[i-2]),
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        #'postag': postag,
        #'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = str(sent)[i-1]
        #postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            #'-1:postag': postag1,
            #'-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = str(sent)[i+1]
        #postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
           # '+1:postag': postag1,
           # '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]
    
'''

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

words = list(data['word'])

# define own special character set 
#regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]./') 
special_chars = ('.',',','(', ')', '–', '[', '·','{', '}', ']', ':', ';', "'", '"','?', '/', '*','!', '@', '#', '&', '"*"', '`', '~', '$', '^', '+', '=', '<', '>','%')

features = {
    'word.lower': [],
    'word.isupper': [],
    'word.istitle': [],
    'word.isdigit': [],
    'word.isdate': [],
    'word.length': [],
    'word.isspecial.char' :[],
    'word.contains.special.char' :[],

    'word[-1]': [],
    '-1:word.lower': [],
    '-1:word.istitle': [],
    '-1:word.isupper': [],
    '-1:word.isspecial.char' :[],

    'word[-2]': [],
    'word[-3]': []
}

for i, w in enumerate(words):
    features['word.lower'].append(str(w).lower())
    features['word.isupper'].append(str(w).isupper())
    features['word.istitle'].append(str(w).istitle())
    features['word.isdigit'].append(str(w).isdigit())

    if is_date(str(w)):
        features['word.isdate'].append(True)
    else:
        features['word.isdate'].append(False)

    features['word.length'].append(len(str(w)))
    if str(w) in special_chars:
        features['word.isspecial.char'].append(True)
    else:
        features['word.isspecial.char'].append(False)
    if any(x in str(w) for x in special_chars):
         features['word.contains.special.char'].append(True)
    else:
        features['word.contains.special.char'].append(False)

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
        
features = pd.DataFrame(features)

print(features.shape)
print(data.shape)

final_data = pd.concat([data, features], axis=1, sort=False)
    

final_data.to_csv('final.csv', encoding='utf-8-sig')


