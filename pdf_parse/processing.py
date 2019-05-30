from tika import parser # PDF parsing package - seems to be better than PyPdf2 and PdfToText
from pandas import DataFrame # Data management package, has useful excel write
import time
import os
from os import listdir

output_dir = os.path.abspath(os.getcwd() + '/Output')

def get_input_file_paths():
	input_dir = listdir(os.path.abspath(os.getcwd() + '/Input'))
	input_file_paths = []
	for file in input_dir:
		input_file_paths.append(os.path.abspath(os.getcwd() + '/Input/' + file))

	return input_file_paths

def process_pdf(input_path, output_path):
	raw = parser.from_file(input_path) # get pdf at specified loaction in path
	text = raw['content'] # get the raw text the parser retrieved
	lines = text.split('\n') # convert the raw text into a list of each newline seperated phrase
	word_bag = {} # dictionary data type -- basically stores (key, value) pairs
	for i, line in enumerate(lines): # walk through the lines
		lines[i] = line.replace('\n', ' ') # clean out the text
		if(lines[i] not in word_bag): # word frequency counting
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
	file_prefix = file_prefix.split('.')[0]
	# make the excel -- it auto saves
	df.to_excel(output_path + '/' + file_prefix + 'output_' + str(time.localtime()[3]) + '_' + str(time.localtime()[5]) + '.xlsx', sheet_name='sheet1', index=False)

def flush_input():
	paths = get_input_file_paths()
	for drawing_path in paths:
		process_pdf(drawing_path, output_dir)
