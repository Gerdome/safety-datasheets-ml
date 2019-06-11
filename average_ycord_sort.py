import pandas as pd
import os


#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/words_detected_ordered/data_0_50_ordered.csv'

#full path to data files
datapath = os.path.join(ospath, datadir)


df = pd.read_csv(datapath)

yc = df['Ycord_first']
yc_new = []

counter = 0
first = True
for index, i in enumerate(yc):

	#very first row
	if first == True:
		avg = i
		counter += 1 
	elif abs(avg - i) <= 5:
		avg = avg - ((avg - i)/(counter+1))
		counter += 1
		#very last row
		if index == (len(yc)-1):
			yc_new += counter * [avg]
	elif abs(avg - i) > 5:
		yc_new += counter * [avg]
		avg = i
		counter = 1


	first = False


df['ycord_average'] = yc_new


df = df.sort_values(['doc','Page','ycord_average','Xcord_first'],ascending=[True,True,False,True])

df.to_csv(os.path.join(ospath,'data/words_detected_ordered/data_0_50_avg_ordered.csv'), encoding ='utf-8-sig')