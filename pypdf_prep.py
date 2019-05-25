import PyPDF2
import os
from nltk.tokenize import word_tokenize


#set directory path of current script
ospath =  os.path.dirname(__file__) 

#specify relative path to data files
datadir = 'data/'

#full path to data files
datapath = os.path.join(ospath, datadir)

#list of all files
entries = os.listdir(datapath)

#open first PDF file
pdfFileObj = open(os.path.join(datapath , '190.pdf'), 'rb')

# read pdf with pdf file reader
pdf = PyPDF2.PdfFileReader(pdfFileObj)

# number of pages in pdf
num_pages = pdf.numPages

#meta info about document
info = pdf.getDocumentInfo()
print(info)

# a page object
page = pdf.getPage(1)

# extracting text from page.
text = page.extractText()
print(text)

tokens = word_tokenize(text)
print(tokens)