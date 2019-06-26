import pandas as pd
import os
import numpy as np


#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files

datadir =  'data/2_final/'

labels = ['chapter','subchapter','chem','company','dates','directive','signal','usecase','version']

labeldata = {}
df = pd.DataFrame()

data = pd.read_csv(os.path.join(ospath, datadir) + '/chapter_identified.csv', dtype=str, index_col = 0)

for l in labels:
    print(l)
    datapath = os.path.join(ospath, datadir) + '/' + l + '_identified.csv'
    d = pd.read_csv(datapath)
    labeldata[str(l)] = list(d[l])



for l in labeldata:
    data[l] = labeldata[l]

    
#data['label'] = data[labels].max(1) #Kurze ausgabe wenn er mehrere ungleich null findet 
#data = data.drop(labels, 1)


for row in data.loc[:,['word']].itertuples(index=True):
    print(row)

    if str(data.loc[row.Index, 'chapter']) == '1.0':
        data.loc[row.Index,'label'] = 1

    elif str(data.loc[row.Index, 'subchapter']) == '1.0':
        data.loc[row.Index,'label'] = 2

    elif str(data.loc[row.Index, 'chem']) == 'cas':
        data.loc[row.Index,'label'] = 3

    elif str(data.loc[row.Index, 'company']) == '1.0':
        data.loc[row.Index,'label'] = 4

    elif str(data.loc[row.Index, 'dates']) == 'Druck':
        data.loc[row.Index,'label'] = 5
    elif str(data.loc[row.Index, 'dates']) == 'Gültig':
        data.loc[row.Index,'label'] = 6
    elif str(data.loc[row.Index, 'dates']) == 'Nicht zuordbar':
        data.loc[row.Index,'label'] = 7
    elif str(data.loc[row.Index, 'dates']) == 'Überarbeitung':
        data.loc[row.Index,'label'] = 8
    elif str(data.loc[row.Index, 'dates']) == 'Vorgänger':
        data.loc[row.Index,'label'] = 9

    elif str(data.loc[row.Index, 'directive']) == '1.0':
        data.loc[row.Index,'label'] = 10
    
    elif str(data.loc[row.Index, 'signal']) == '1.0':
        data.loc[row.Index,'label'] = 11
    
    elif str(data.loc[row.Index, 'usecase']) == 'usecase_pro':
        data.loc[row.Index,'label'] = 12
    elif str(data.loc[row.Index, 'usecase']) == 'usecase_con':
        data.loc[row.Index,'label'] = 13
    
    elif str(data.loc[row.Index, 'version']) == 'version':
        data.loc[row.Index,'label'] = 14

'''
for l in labeldata:
    print(len(labeldata[l]))
    for i, j in enumerate(labeldata[l]):
        print(i)
        if j != '0':
            data.loc[i,'label'] = j
'''

data.to_csv('labeled_data.csv', encoding='utf-8-sig')


