# from tika import parser # PDF parsing package - seems to be better than PyPdf2 and PdfToText
import pandas as pd
from pandas import DataFrame # Data management package, has useful excel write
import datetime
import os
from os import listdir

output_dir = os.path.abspath(os.getcwd() + '/Output')

def get_phrases():
	phrases = []
	f = open("pdf_parse/phrases.txt", "r")
	for line in f:
		phrases.append(line.strip())
	return phrases

def get_input_file_paths():
	''' Pre chill, just grabs all the files in the input directory
	'''
	input_dir = listdir(os.path.abspath(os.getcwd() + '/Input')) # get the absolute path to the input folder
	input_file_paths = []
	for file in input_dir:
		input_file_paths.append(os.path.abspath(os.getcwd() + '/Input/' + file)) # put all the input file paths in a list
	return input_file_paths # return said list of input file paths

def process_pdf(input_path):
	''' Process the pdf at the given path. Returns the filename and the phrases, frequencies
	'''
	import pdftotext
	with open(input_path, 'rb') as f:
		pdf = pdftotext.PDF(f)
	# text = pdf.read_all()
	text = pdf[0]
	# raw = parser.from_file(input_path) # get pdf at specified loaction in path
	# text = raw['content'] # get the raw text the parser retrieved
	# convert the raw text into a list of each newline seperated phrase
	lines = (''.join(text.split('\n'))).split('  ')
	lines = [x.strip() for x in lines]
	temp = []
	for x in lines:
		if(len(x) > 0):
			temp.append(x)
	lines = temp
	# print(lines)
	word_bag = {} # dictionary data type -- basically stores (key, value) pairs
	desired_phrases = get_phrases()
	for i, line in enumerate(lines): # walk through the lines
		lines[i] = line.replace('\n', ' ') # clean out the text
		if(lines[i] not in word_bag): # word frequency counting
			# phrase lookup
			if(lines[i] in desired_phrases):
				word_bag[lines[i]] = 1
		else:
			word_bag[lines[i]] += 1

	skrrt = []
	for k, v in word_bag.items(): # toss the phrases, frequencies into a list for sorting (since dictionaries are unsorted)
		skrrt.append([v, k])
	skrrt = sorted(skrrt, key = lambda x: int(x[0]), reverse=True) # sort this baddy
	freqs = [x[0] for x in skrrt] # get the frequencies
	phrases = [x[1] for x in skrrt] # get the phrases

	df = DataFrame({'Phrase' : phrases, 'Frequency' : freqs}) # create the data frame
	file_prefix = input_path.split('/')[len(input_path.split('/')) - 1] # get the file name prefix
	file_prefix = ''.join(file_prefix.split('.')[:1])

	return [file_prefix, df]
	
def produce_excel(procced_drawings, output_path, multi_worksheet=True):
	''' Given a list of tuples containing the drawing name (file_prefix) and the dataframe (phrases and frequencies)
		this will create the excel in one of two ways. Either mutli-worksheet in the same workbook or in the same 
		worksheet, with drawing seperations being blank columns
	'''
	with pd.ExcelWriter(output_path + '/output_' + datetime.datetime.now().strftime('%a%b%Y%H%M%S') + '.xlsx', engine="xlsxwriter") as writer:
		if(multi_worksheet):
			for file_prefix, df in procced_drawings:
				if(len(file_prefix) > 31): # length check due to worksheet name length limit
					file_prefix = file_prefix[:len(file_prefix)-31] # prune the name to at most 31 characters
				df.to_excel(writer, sheet_name=file_prefix, index=False)
		else:
			startcol = 0
			for file_prefix, df in procced_drawings:
				pd.DataFrame([file_prefix], index=["Drawing Name"]).to_excel(writer, startcol=startcol, startrow=0, index=True, header=False)
				df.to_excel(writer, startcol=startcol, startrow=1, index=False, header=True)
				startcol += df.shape[1] + 2

def input_file_check(path):
	''' Checks if files in the input directory have already been processed, lil QOL
	'''
	filename = path.split('/')[-1]
	if(filename[0] == "_"):
		return False
	else:
		return True

def input_file_flag(path):
	''' Flags files that have been processed in the Input directory by prepending a '_' before the file
	'''
	filename = path.split('/')[-1]
	new_path = '/'.join(path.split('/')[:-1]) + '/_' + filename
	os.rename(path, new_path)

def flush_input():
	''' Temporary input processing, will be more robust with more options later
	'''
	paths = get_input_file_paths() # get all drawing file paths
	procced_drawings = []
	for drawing_path in paths:
		if(input_file_check(drawing_path)): # check if it has been processed, if not, continue
			procced_drawings.append(process_pdf(drawing_path))
	
	produce_excel(procced_drawings, output_dir, False)
	# for drawing_path in paths: # mark all files that were processed to avoid re-processing
		# input_file_flag(drawing_path)

