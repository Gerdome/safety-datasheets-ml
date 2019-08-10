import pandas as pd
import numpy as np
import os 
import re

paper_feature = ['is.lower', 'is.upper', 'is.mixed.case', 'is.digit', 'contains.digit', 'is.special.char', 'len.1.2', 'len.3.4', 'len.5.6', 'len.7.8', 'len.9.10', 'len.11.13', 'len.13', 'is.stop']

date_specific_feature = ['is.print.date.trigger', 'is.revision.date.trigger', 'is.valid.date.trigger', 'is.old.version.date']

new_feature = ['contains.special.char','is.title', 'is.bold', 'is.newline','ycord_average','Xcord_first', 'koord.1', 'koord.2', 'koord.3', 'koord.4', 'koord.5', 'koord.6', 'koord.7', 'koord.8', 'is.page.1', 'is.page.2', 'is.page.3']



def prepare_data (filename):

    #set directory path of current script
    ospath =  os.path.dirname(__file__) 

    #specify relative path to data files
    datadir = 'data/2_final/'

    #full path to data files
    datapath = os.path.join(ospath, datadir)

    #read raw data csv
    data = pd.read_csv(datapath + filename, encoding='utf-8-sig', index_col=0)

    return data

def sample_window (data, window_size):

    last_col = int(window_size/2)
    #change to final starting and ending points
    sample_data = data.loc[:, 'word.is.lower':('+' + str(last_col) + '_word.is.newline')]

    return sample_data

def sample_features (data):
    

def main ():
    
    data = prepare_data('data_all_labeled.csv')

    
if __name__ == '__main__':
    main()