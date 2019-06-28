import pandas as pd
import numpy as np
import os 
import re

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