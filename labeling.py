import pandas as pd
import numpy as np
import os 
import re

labels = ['chap', #1
        'subchapter',#2
        'chemicals',#3
        'company',#4
        'date',#5
        'directive',#6
        'signal',#7
        'usecase',#8
        'version']#9

for l in labels:
    print(l)
    os.system("c:/Users/merzg/FZI_Seminar/safetysheets/env/Scripts/python.exe c:/Users/merzg/FZI_Seminar/safetysheets/safety-datasheets-ml/" + str(l) + "_identifier.py")