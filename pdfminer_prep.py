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
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextBoxHorizontal, LTFigure
from pdfminer.converter import PDFPageAggregator

import pandas as pd

''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page 
'''


#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#list of all files
entries = os.listdir(datapath)

#define empty lists
pages = []
xcord = []
ycord = []
content = []
docs = []
i = 0

password = ""
extracted_text = ""

def parse_obj(lt_objs):
	# loop over the object list
	for obj in lt_objs:

		# if it's a textbox, print text and location
		if isinstance(obj, LTTextBoxHorizontal):
			#print (str(p) +',' +"%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))
			pages.append(pagenum)
			xcord.append(obj.bbox[0])
			ycord.append(obj.bbox[1])
			content.append(obj.get_text().replace('\n', '_'))
			docs.append(docnr)
			#df = df.append({'page': pagenum, 'Xcord': obj.bbox[0], 'Ycord': obj.bbox[1], 'Content':obj.get_text().replace('\n', '_') }, ignore_index=True)


		# if it's a container, recurse
		elif isinstance(obj, LTFigure):
			parse_obj(obj._objs)


for d, entry in enumerate(entries):
	print(entry)
	print(i)

	docnr = d + 1

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
	for p ,page in enumerate(PDFPage.create_pages(document)):
		pagenum = p + 1
		# As the interpreter processes the page stored in PDFDocument object
		interpreter.process_page(page)
		# The device renders the layout from interpreter
		layout = device.get_result()

		# extract text from this object
		parse_obj(layout._objs)
		# # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
		# for lt_obj in layout:
		# 	if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
		# 		extracted_text += lt_obj.get_text()
				
	#close the pdf file
	fp.close()

	i = i+1


#creat empty dataframe
df = pd.DataFrame( 
	{
	 'doc': docs,
	 'Page': pages,
     'Xcord': xcord,
     'Ycord': ycord,
	 'Content': content,
    })


df.to_csv('test.csv', index=False)
