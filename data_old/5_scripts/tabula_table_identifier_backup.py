from tabula import read_pdf
import pandas as pd
import os

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/3_pdf/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#list of all files
entries = os.listdir(datapath)

for i, entry in enumerate(entries[3:6]):
    df = read_pdf(os.path.join(datapath , entry ), pages=[1,2,3])
    df.to_csv('table_'+ str(entry) + '.csv', encoding='utf-8-sig')