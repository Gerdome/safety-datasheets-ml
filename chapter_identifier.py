import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/1_working/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'data_0_50_avg_ordered.csv', dtype=str, index_col = 0)

#get list of all words
words = list(data['word'])

#Stop words removal
# stopWords = set(stopwords.words('german'))
# filtered_words = [w for w in words if not w in stopWords] 
# freqDist = FreqDist(filtered_words)
# print(freqDist.most_common(50))

#### Simple Case --> Just look for name of each chapter (e.g: 'Bezeichnung des Stoffs')

##############  Identify upper case headers  ############## 
# --> identify ones with ":" after ABSCHNITT (ABSCHNITT 1:, ABSCHNITT 13:)

cap_chapters1 = {}
cap_chapters2 = {}
cap_chapters3 = {}
cap_chapters4 = {}
cap_chapters5 = {}
cap_chapters6 = {}

for c in range(16):
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == 'ABSCHNITT' and str(words[i + 1])[:2] == (str(c+1) + ':' if (c+1) < 10 else str(c+1)):
             l1.append(i)
    cap_chapters1[c+1] = l1



##############  Identify upper case headers  ############## 
# --> identify ones without ":" after ABSCHNITT (only a few)

for c in range(16):
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == 'ABSCHNITT' and str(words[i + 1]) == str(c+1):
             l1.append(i)
    cap_chapters2[c+1] = l1
 

##############  Identify lower case headers  ###############  --> could be also somewhere else --> also check preceding word
#  --> if in the text often: Siehe unter Abschnitt 12 
# Siehe Abschitt 
# ist dem Abschnitt 12 zu entnehmen 
# nach Abschnitt 12 
# auf Abschnitt 12

#Bei Pruefen auf '' vor dem Abschnitt gibts keine Optionen mehr

# --> Scheint keine Ueberschriften in dieser Variante zu geben

for c in range(16):
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == 'Abschnitt' and str(words[i-1]) != 'auf' and str(words[i-1]) != 'nach' and str(words[i-1]) != 'dem'  and str(words[i-1]) != 'Siehe' and str(words[i-1]) != 'siehe'  and str(words[i-1]) != 'unter'  and str(words[i + 1]) == str(c+1):
             l1.append(i)
    cap_chapters3[c+1] = l1

##############  Identify upper case headers  ############## 
# --> identify ones with ":" after ABSCHNITT and 0 if single character (ABSCHNITT 01:, ABSCHNITT 13:)


for c in range(16):
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == 'ABSCHNITT' and str(words[i + 1])[:2] == '0' + (str(c+1) ):
             l1.append(i)
    cap_chapters4[c+1] = l1


##############  Identify chapter headers without 'ABSCHNITT'  ############## 
# --> Take first word of header and check if preceding word is number
#  
# Dictionary of first word for each chapter
header_words = {
    1: 'Bezeichnung',
    2: 'Mögliche',
    3: 'Zusammensetzung/Angaben',
    4: 'Erste-Hilfe-Maßnahmen',
    5: 'Maßnahmen', # Massnahmen auch moeglich
    6: 'Maßnahmen', 
    7: 'Handhabung',
    8: 'Begrenzung',
    9: 'Physikalische',
    10: 'Stabilität',
    11: 'Toxikologische',
    12: 'Umweltbezogene',
    13: 'Hinweise',
    14: 'Angaben',
    15: 'Rechtsvorschriften',
    16: 'Sonstige'}
    
header_cap_words = {
    1: 'BEZEICHNUNG',
    2: 'MÖGLICHE',
    3: 'ZUSAMMENSETZUNG/ANGABEN',
    4: 'ERSTE-HILFE-MAßNAHMEN',
    5: 'MAßNAHMEN', # Massnahmen auch moeglich
    6: 'MAßNAHMEN', 
    7: 'HANDHABUNG',
    8: 'BEGRENZUNG',
    9: 'PHYSIKALISCHE',
    10: 'STABILITÄT',
    11: 'TOXIKOLOGISCHE',
    12: 'UMWELTBEZOGENE',
    13: 'HINWEISE',
    14: 'ANGABEN',
    15: 'RECHTSVORSCHRIFTEN',
    16: 'SONSTIGE'}

for c in range(16):
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == header_words[c+1] and str(words[i - 1]) == (str(c+1) ):
             l1.append(i)
    cap_chapters5[c+1] = l1


for c in range(16):
    l1 = []
    for i, e in enumerate(words):       
        if words[i] == header_cap_words[c+1] and str(words[i - 1]) == (str(c+1) ):
             l1.append(i)
    cap_chapters6[c+1] = l1


## Combine all identifiers
cap_chapter = {}

for i in range(16):
    #combine all identified headers for each chapter
    l1 = cap_chapters1[i+1] + cap_chapters2[i+1] + cap_chapters3[i+1] + cap_chapters4[i+1] + cap_chapters5[i+1] + cap_chapters6[i+1]
    #sort them
    l1.sort()
    #save in dictionary
    cap_chapter[i+1] = l1


# fill in identified labels in data
data['label'] = '0'
for i in range(16):
    for j in cap_chapter[i+1]:
        data.loc[j,'label'] = 'Header Chapter ' + str(i+1)

data.to_csv('chapter_identified.csv', encoding='utf-8-sig')

