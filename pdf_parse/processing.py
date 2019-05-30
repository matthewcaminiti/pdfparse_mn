from tika import parser # PDF parsing package - seems to be better than PyPdf2 and PdfToText
from pandas import DataFrame # Data management package, has useful excel write

def process_pdf(path):
	raw = parser.from_file(path) # get pdf at specified loaction in path
	text = raw['content'] # get the raw text the parser retrieved
	lines = text.split('\n') # convert the raw text into a list of each newline seperated phrase
	word_bag = {} # dictionary data type -- basically stores (key, value) pairs
	for i, line in enumerate(lines): # walk through the lines
		lines[i] = line.replace('\n', ' ') # clean out the text
		if(lines[i] not in word_bag): # word frequency counting
			word_bag[lines[i]] = 1
		else:
			word_bag[lines[i]] += 1

	# for x in lines: print("[%s]" % x)

	skrrt = []
	for k, v in word_bag.items(): # toss the phrases, frequencies into a list for sorting (since dictionaries are unsorted)
		skrrt.append([v, k])

	skrrt = sorted(skrrt, key = lambda x: int(x[0]), reverse=True) # sort this baddy

	freqs = [x[0] for x in skrrt] # get the frequencies
	phrases = [x[1] for x in skrrt] # get the phrases

	df = DataFrame({'Phrase' : phrases, 'Frequency' : freqs}) # create the data frame
	file_prefix = path.split('/')[len(path.split('/')) - 1] # get the file name prefix
	file_prefix = file_prefix.split('.')[0]
	# make the excel -- it auto saves
	df.to_excel(file_prefix + 'output_' + str(time.localtime()[3]) + '_' + str(time.localtime()[5]) + '.xlsx', sheet_name='sheet1', index=False)

