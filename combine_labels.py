import pandas as pd
import os
import numpy as np


#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir =  'data/2_final/'

labels = ['chapter','subchapter','version','dates']
labeldata = {}
df = pd.DataFrame()

data = pd.read_csv(os.path.join(ospath, datadir) + '/dates_identified.csv', dtype=str, index_col = 0)

for l in labels:
    datapath = os.path.join(ospath, datadir) + '/' + l + '_identified.csv'
    d = pd.read_csv(datapath)
    labeldata[str(l)] = list(d[l])



for l in labeldata:
    data[l] = labeldata[l]
    
data['label'] = data[labels].max(1) #Kurze ausgabe wenn er mehrere ungleich null findet 
data = data.drop(labels, 1)



'''
for l in labeldata:
    print(len(labeldata[l]))
    for i, j in enumerate(labeldata[l]):
        print(i)
        if j != '0':
            data.loc[i,'label'] = j
'''

data.to_csv('labeled_data.csv', encoding='utf-8-sig')


