from datetime import datetime
import pandas as pd
import numpy as np
from nltk import FreqDist
from nltk.corpus import stopwords
import os 
import re
from operator import itemgetter
from sklearn_crfsuite import CRF
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import json
import csv




#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/2_final/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'final.csv', dtype=str, encoding='utf-8-sig', index_col=0)

features = [
    'word',
    'Xcord_first', 'ycord_average',  
    'word.isupper','word.istitle','word.isdigit',
    'word[-1]','-1:word.istitle','-1:word.isupper', 
    'word[-2]',
    'word[-3]',
    ]

data.fillna(0)

#categorize alphabetic features
data = data.astype('category')

#save features categories in dictioniary
word_code_dict = dict(enumerate(data['word'].cat.categories))
#save features categories in dictioniary
label_code_dict = dict(enumerate(data['label'].cat.categories))

with open('label_dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in label_code_dict.items():
       writer.writerow([key, value])
'''
with open('word_dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in word_code_dict.items():
       writer.writerow([key, value])
'''
data['word'] = data['word'].cat.codes
data['word.isupper'] = data['word.isupper'].cat.codes
data['word.istitle'] = data['word.istitle'].cat.codes
data['word.isdigit'] = data['word.isdigit'].cat.codes

data['word[-1]'] = data['word[-1]'].cat.codes
data['-1:word.lower'] = data['-1:word.lower'].cat.codes
data['-1:word.istitle'] = data['-1:word.istitle'].cat.codes
data['-1:word.isupper'] = data['-1:word.isupper'].cat.codes

data['word[-2]'] = data['word[-2]'].cat.codes

data['word[-3]'] = data['word[-3]'].cat.codes


#categorize labels
data['label'] = data['label'].cat.codes


# Separating out the features
X = data.loc[:, features]
# Separating out the target
y = data.loc[:,['label']]

# create multiple labels for different categories
# version is 72
y = y['label'].apply(lambda x: 1 if x == 72 else 0)

#train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

'''
crf = CRF(algorithm='lbfgs',
          c1=0.1,
          c2=0.1,
          max_iterations=100,
          all_possible_transitions=False)
    
crf.fit(X_train, y_train)
        
'''

classifier = RandomForestClassifier()

classifier.fit(X_train, y_train)


y_pred = classifier.predict(X_test)

print(y_pred)

score = classifier.score(X_test, y_test)
print(score)

cm = metrics.confusion_matrix(y_test, y_pred)
print(cm)



# Use sckit classification report for showing accuracy
print(classification_report(y_pred=y_pred, y_true=y_test))

'''
plt.figure(figsize=(9,9))
sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 15);
'''