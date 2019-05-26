import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import os 

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#read raw data csv
data = pd.read_csv(datapath + 'full_data_0_50.csv')

#get list of all words
words = list(data['Content'])

#Stop words removal
# stopWords = set(stopwords.words('german'))
# filtered_words = [w for w in words if not w in stopWords] 
# freqDist = FreqDist(filtered_words)
# print(freqDist.most_common(50))

#### Simple Case --> Just look for name of each chapter (e.g: 'Bezeichnung des Stoffs')

##############  Identify upper case headers  ############## --> definitely header of chapter
print(words.index('ABSCHNITT'))
cap_chapters = [i for i, e in enumerate(words) if e == 'ABSCHNITT']
print(cap_chapters)

##############  Identify lower case headers  ###############  --> could be also somewhere else
chapters = [i for i, e in enumerate(words) if e == 'Abschnitt']
### check whether it's the start of a line (object) and followed by a number

# identify 1s
firstchapters = [i for i, e in enumerate(words) if e == '1']
print(firstchapters)
# identify 1s with empty space/newline before and Information right after it --> likely to be header of chapter

