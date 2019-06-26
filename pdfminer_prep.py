# pdfTextMiner.py
# Python 2.7.6
# For Python 3.x use pdfminer3k module
# This link has useful information on components of the program
# https://euske.github.io/pdfminer/programming.html
# http://denis.papathanasiou.org/posts/2010.08.04.post.html


''' Important classes to remember
PDFParser - fetches data from pdf file
PDFDocument - stores data parsed by PDFParser
PDFPageInterpreter - processes page contents from PDFDocument
PDFDevice - translates processed information from PDFPageInterpreter to whatever you need
PDFResourceManager - Stores shared resources such as fonts or images used by both PDFPageInterpreter and PDFDevice
LAParams - A layout analyzer returns a LTPage object for each page in the PDF document
PDFPageAggregator - Extract the decive to page aggregator to get LT object elements
'''

import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextBoxHorizontal, LTFigure, LTChar, LTText, LTAnno
from pdfminer.converter import PDFPageAggregator
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize

''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page 
'''

'''
pdf nr: 42, 72, 124, 145,259, 298, 368, 369, 450, 451, 605, 623 not in data ! 
'''

#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/3_pdf/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#list of all files
entries = os.listdir(datapath)

#define empty lists
pages = []
xcord = []
ycord = []
xcords_first = []
ycords_first = []
font_size = []
font_names = []
content = []
docs = []
objects = []
textboxes = []
i = 0
words = []

password = ""
extracted_text = ""

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def parse_obj(lt_objs):
	objectnum = 1
	# loop over the object list
	for obj in lt_objs:

		# if it's a textbox, print text and location
		if isinstance(obj, LTTextBoxHorizontal):
			pages.append(pagenum)
			xcord.append(obj.bbox[0])
			ycord.append(obj.bbox[1])
			content.append(obj.get_text().replace('\n', ' _ '))
			docs.append(doc)
			objects.append(objectnum)

		# if it's a container, recurse
		elif isinstance(obj, LTFigure):
			parse_obj(obj._objs)

		objectnum = objectnum + 1


def parse_words(lt_objs):
        objectnum = 1
        #iterate through Textboxes
        for obj in lt_objs:
                textboxnum = 1
                if isinstance(obj, LTTextBoxHorizontal):
                #iterate through TextLines
                        for o in obj._objs:
                                if isinstance(o, LTTextLine):
                                        text=o.get_text()
                                        #print(text)
                                        if text.strip():
                                                word = ''
                                                #iterate through characters
                                                for c in  o._objs:
                                                        #if it is a character
                                                        if isinstance(c, LTChar):
                                                                #detect special character at end of words
                                                                if c.get_text() in (')',':','%',';','('):
                                                                    words.extend([word, str(c.get_text())])
                                                                    pages.extend([pagenum, pagenum])
                                                                    xcords_first.extend([xcord_first,c.bbox[0]])
                                                                    ycords_first.extend([ycord_first,c.bbox[1]])
                                                                    docs.extend([doc, doc])
                                                                    font_size.extend([fontsize,int(round(c.fontsize))])
                                                                    font_names.extend([fontname,c.fontname])
                                                                    objects.extend([objectnum, objectnum])
                                                                    textboxes.extend([textboxnum, textboxnum])
                                                                    word = ''
                                                                # if / in between of numbers --> not a new token
                                                                elif c.get_text() in ('/') and not word.isdigit() and not word == 'g':
                                                                    words.extend([word, str(c.get_text())])
                                                                    pages.extend([pagenum, pagenum])
                                                                    xcords_first.extend([xcord_first,c.bbox[0]])
                                                                    ycords_first.extend([ycord_first,c.bbox[1]])
                                                                    docs.extend([doc, doc])
                                                                    font_size.extend([fontsize,int(round(c.fontsize))])
                                                                    font_names.extend([fontname,c.fontname])
                                                                    objects.extend([objectnum, objectnum])
                                                                    textboxes.extend([textboxnum, textboxnum])
                                                                    word = ''
                                                                # if , in between of numbers --> not a new token
                                                                elif c.get_text() in (',') and not word.isdigit():
                                                                    words.extend([word, str(c.get_text())])
                                                                    pages.extend([pagenum, pagenum])
                                                                    xcords_first.extend([xcord_first,c.bbox[0]])
                                                                    ycords_first.extend([ycord_first,c.bbox[1]])
                                                                    font_size.extend([fontsize,int(round(c.fontsize))])
                                                                    font_names.extend([fontname,c.fontname])
                                                                    docs.extend([doc, doc])
                                                                    objects.extend([objectnum, objectnum])
                                                                    textboxes.extend([textboxnum, textboxnum])
                                                                    word = ''
                                                                
                                                                # take 'n.v' as an exception and check that . is not in between numbers or dates
                                                                elif c.get_text() in ('.') and not hasNumbers(word) and not word == 'n' and '@' not in word:
                                                                    words.extend([word, str(c.get_text())])
                                                                    pages.extend([pagenum, pagenum])
                                                                    xcords_first.extend([xcord_first,c.bbox[0]])
                                                                    ycords_first.extend([ycord_first,c.bbox[1]])
                                                                    font_size.extend([fontsize,int(round(c.fontsize))])
                                                                    font_names.extend([fontname,c.fontname])
                                                                    docs.extend([doc, doc])
                                                                    objects.extend([objectnum, objectnum])
                                                                    textboxes.extend([textboxnum, textboxnum])
                                                                    word = ''
                                                                    
                                                                else:
                                                                    #append until space
                                                                    word += str(c.get_text())
                                                                    #remember coords if its first char of word
                                                                    if len(word) == 1:
                                                                            xcord_first = c.bbox[0]
                                                                            ycord_first = c.bbox[1]
                                                                            fontsize = int(round(c.fontsize))
                                                                            fontname = c.fontname
                                                                    # if space and previous token was not space: append word to list (without the space) and start new word
                                                                    if c.get_text() == ' ':
                                                                            words.append(word[:-1])
                                                                            pages.append(pagenum)
                                                                            xcords_first.append(xcord_first)
                                                                            ycords_first.append(ycord_first)
                                                                            font_size.append(fontsize)
                                                                            font_names.append(fontname)
                                                                            docs.append(doc)
                                                                            objects.append(objectnum)
                                                                            textboxes.append(textboxnum)
                                                                            word = ''
                                                        #if it is a new line and word is not empty: append word to list and start new word
                                                        if isinstance(c, LTAnno):
                                                                words.append(word)
                                                                pages.append(pagenum)
                                                                xcords_first.append(xcord_first)
                                                                ycords_first.append(ycord_first)
                                                                font_size.append(fontsize)
                                                                font_names.append(fontname)
                                                                docs.append(doc)
                                                                objects.append(objectnum)
                                                                textboxes.append(textboxnum)
                                                                word = ''
             
                                textboxnum = textboxnum + 1
                                                                                         
                # if it's a container, recurse
                elif isinstance(obj, LTFigure):
                        parse_words(obj._objs)

                objectnum = objectnum + 1

for d, entry in enumerate(entries):
	print(entry)

	doc = entry

	#open first PDF file
	fp = open(os.path.join(datapath , entry), 'rb')


	# Create parser object to parse the pdf content
	parser = PDFParser(fp)

	# Store the parsed content in PDFDocument object
	document = PDFDocument(parser, password)
		
	# Create PDFResourceManager object that stores shared resources such as fonts or images
	rsrcmgr = PDFResourceManager()

	# set parameters for analysis
	laparams = LAParams()

	# Create a PDFDevice object which translates interpreted information into desired format
	# Device needs to be connected to resource manager to store shared resources
	device = PDFDevice(rsrcmgr)
	# Extract the decive to page aggregator to get LT object elements
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)

	# Create interpreter object to process page content from PDFDocument
	# Interpreter needs to be connected to resource manager for shared resources and device 
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	# Ok now that we have everything to process a pdf document, lets process it page by page
	# process only first 3 pages 
	for p ,page in enumerate(PDFPage.create_pages(document)):
		pagenum = p + 1        
		if pagenum == 4:
			break
		# As the interpreter processes the page stored in PDFDocument object
		interpreter.process_page(page)
		# The device renders the layout from interpreter
		layout = device.get_result()

		# call function to parse on character level
		parse_words(layout._objs)
	
		# call function to parse on text box level
		#parse_obj(layout._objs)
				
	#close the pdf file
	fp.close()

	i = i+1

print(len(docs))
print(len(font_size))
print(len(font_names))
#creat empty dataframe
df = pd.DataFrame( 
	{
	 'doc': docs,
	 'Page': pages,
	 'Ycord_first': ycords_first,
        'Xcord_first': xcords_first,
        'font_size': font_size,
        'font_name': font_names,
	 'Object': objects,
        'Textbox': textboxes,
	 'word': words
    })

df = df.sort_values(['doc','Page','Ycord_first','Xcord_first'],ascending=[True,True,False,True])

#delete empty tokens
df = df[ df["word"] != ""]

#identify special characters
df['special_char'] = df['word'].apply(lambda x: 1 if (x in ('"*"', 'ꞏ') or (len(x) == 1 and x.isalnum () == False)) else 0 )
#= df['word'].apply(lambda x: 1 if x in ('.',',','(', ')', '–', '[', '·','{', '}', ']', ':', ';', "'", '"','?', '/', '*','!', '@', '#', '&', '"*"', '`', '~', '$', '^', '+', '=', '<', '>', 'ꞏ') else 0 )

df.to_csv('data_all_ordered.csv', encoding='utf-8-sig')

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

yc_new.append(yc_new[-1])

print(len(yc_new))
print(df.shape)

df['ycord_average'] = yc_new


df = df.sort_values(['doc','Page','ycord_average','Xcord_first'],ascending=[True,True,False,True])

df.reset_index(inplace=True, drop = True)

df.to_csv('data_all_avg_ordered.csv', encoding='utf-8-sig')