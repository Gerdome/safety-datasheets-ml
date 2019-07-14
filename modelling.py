# Models
from sklearn.svm import LinearSVC #SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
# Other Packages
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.externals import joblib
import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# Label mappings
label_group_dict = { 0: 0,
                     1: 'chapter',
                     2: 'company',
                     3: 'directive',
                     4: 'signal',
                     5: 'subchapter',
                     6: 'usecase_con',
                     7: 'usecase_pro',
                     8: 'version'}

date_dict = {0: 0,
             1: 'oldversiondate',
             2: 'validdate',
             3: 'printdate',
             4: 'revisiondate'}

def set_feature_rng (data):
    # Ranges Feature
    colidx = data.columns.get_loc
    # No window
    r_paper = np.r_[colidx('word.is.lower'):colidx('word.is.stop')]
    r_own = np.r_[colidx('word.is.bold'):colidx('is.page.3')]
    r_own_date_spe = np.r_[colidx('word.is.print.date.trigger'):colidx('word.is.oldversion.date.trigger')]
    r_own_date_full = np.r_[r_own, r_own_date_spe]
    r_web = np.r_[colidx('0'):colidx('299')]

    feature_selection = [('Paper', r_paper),
                        ('Own', r_own),
                        ('Wordembedding', r_web),
                        ('Own+Paper', np.r_[r_own, r_paper]),
                        ('Own+Wordembedding', np.r_[r_own, r_web]),
                        ('Paper+Wordembedding', np.r_[r_paper, r_web]),
                        ('Own+Paper+Wordembedding', np.r_[r_own, r_paper, r_web]),
                        ('date_Paper', r_paper),
                        ('date_Own_std', r_own),
                        ('date_Own_spe', r_own_date_spe),
                        ('date_Own_full', r_own_date_full),
                        ('date_Own_full+Paper', np.r_[r_own_date_full, r_paper]),
                        ('date_Own_full+Wordembedding', np.r_[r_own_date_full, r_web]),
                        ('date_Paper+Wordembedding', np.r_[r_paper, r_web]),
                        ('date_Own_full+Paper+Wordembedding', np.r_[r_own_date_full, r_paper, r_web]),
                        ]

    return feature_selection

def set_feature_rng_w (data):
    # Ranges Feature
    colidx = data.columns.get_loc

    # With window
    r_paper_w = np.r_[colidx('word.is.lower'):colidx('+6_word.is.stop')]
    r_own_w = np.r_[colidx('word.is.bold'):colidx('+6_is.page.3')]
    r_own_date_spe_w = np.r_[colidx('word.is.print.date.trigger'):colidx('+6_word.is.oldversion.date.trigger')]
    r_own_date_full_w = np.r_[r_own_w, r_own_date_spe_w]
    r_web_w = np.r_[colidx('0'):colidx('+1_299')]

    feature_selection_w = [('Paper', r_paper_w),
                        ('Own', r_own_w),
                        ('Wordembedding', r_web_w),
                        ('Own+Paper', np.r_[r_own_w, r_paper_w]),
                        ('Own+Wordembedding', np.r_[r_own_w, r_web_w]),
                        ('Paper+Wordembedding', np.r_[r_paper_w, r_web_w]),
                        ('Own+Paper+Wordembedding', np.r_[r_own_w, r_paper_w, r_web_w]),
                        ('date_Paper', r_paper_w),
                        ('date_Own_std', r_own_w),
                        ('date_Own_spe', r_own_date_spe_w),
                        ('date_Own_full', r_own_date_full_w),
                        ('date_Own_full+Paper', np.r_[r_own_date_full_w, r_paper_w]),
                        ('date_Own_full+Wordembedding', np.r_[r_own_date_full_w, r_web_w]),
                        ('date_Paper+Wordembedding', np.r_[r_paper_w, r_web_w]),
                        ('date_Own_full+Paper+Wordembedding', np.r_[r_own_date_full_w, r_paper_w, r_web_w]),
                        ]
    
    return feature_selection_w

def prepare_data (data, sample_size): #max sample_size = 527
    # Create Dataframe of unique docs to use sample function from pandas with random state
    docs = pd.DataFrame(data.doc.unique())
    random_docs = docs[0].sample(n=sample_size, random_state=1).values.tolist()
    data_sample = data[data['doc'].isin(random_docs)]
    data_sample1 = data_sample.loc[:, 'doc':'chem']
    data_sample2 = data_sample.loc[:, 'word.is.lower':data.iloc[:,-1].name]

    # Replace missing values
    data_sample2 = data_sample2.fillna(data_sample2.mode().iloc[0])
    data_sample = pd.concat([data_sample1, data_sample2], axis=1, sort=False)

    # Split random_docs in test and training sets
    docs_train, docs_test = train_test_split(random_docs, random_state=1)

    # Split random_data in test and training sets
    train, test = data_sample[data_sample['doc'].isin(docs_train)], data_sample[data_sample['doc'].isin(docs_test)]
    
    return train, test

def train_model (feat,lab):
    print ('   **************************Label:' + lab + '**************************')
    # Separate random_data training/test split in features and labels
    x_train = train.iloc[:, feat[1]]
    x_test = test.iloc[:, feat[1]]
    y_train = train.loc[:, lab]
    y_test = test.loc[:, lab]

    # Balance classes
    #smote = SMOTE('minority')
    #x_sm, y_sm = smote.fit_sample(x_train, y_train)

    # training
    start = timer()
    clf = RandomForestClassifier(n_estimators=25)
    clf.fit (x_train, y_train)
    #clf.fit(x_sm, y_sm)
    y_pred = clf.predict(x_test)
    end = timer()
    print('Seconds for training:', end - start)

    # scores
    print(classification_report(y_pred=y_pred, y_true=y_test))

    # Output a pickle file for the model
    joblib.dump(clf, './models/'+ feat[0] + '_' + lab + '.pkl')

def start_training (feature_selection, lab):
    for feat in feature_selection:
        print ('*******************************Features:' + feat[0] + '*******************************')
    
        if feat[0].startswith('date'):
            train_model(feat,'date')
        else:
            for l in lab:
                train_model(feat,l)

print ('***************************************NO_WINDOW***************************************')
data = pd.read_pickle('data_model_allfeatw13_4_web.pkl')
data

feature_selection = set_feature_rng(data)
train, test = prepare_data(data, 527)
start_training(feature_selection, ['label_group', 'chem', 'date'])