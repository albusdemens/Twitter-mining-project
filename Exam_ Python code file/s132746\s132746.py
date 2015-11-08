import string 
import urllib2
import nltk # install nltk, http://nltk.org/install.html
import re
# re is regular expression operation, which specifies a set of strings that matches it
# this is done by the module in the function, which checks if a specific string matches a given regular expression.
# This operation will be used to make anaysis of a text, where fx symbols should not be included.

def main():
	
	print "S132746:" 
	# this will import the url text
	response = urllib2.urlopen('http://www.gutenberg.org/cache/epub/139/pg139.txt') 
	html = response.read()

	# The match object will return a object that matches regular expression pattern
	# the re. search will scan through the string and looking for matches. 
	match = re.search('(p|P)roduced [\-\.\,\w ]+', html) 
	match2 = re.search('\*\*\*\ END OF THIS PROJECT GUTENBERG EBOOK THE LOST WORLD', html)
	#print match
	txt = html[match.end():match2.start()]
	#print txt
	words_dialog(txt)


def words_dialog(txt): 

	# This will make an anlysis for words that are in a dialog, meaning sentence bewteen " "
	# After searching the text for dialogs, it will analysis the top 20 of words that oocur the most.

	collected_tokens = []
	matches = re.finditer('\"[^"]+\"', txt) # the re.finditer matches the words that are dialog between " "
	for match in matches:
		match.group(0) 
		collected_tokens += nltk.word_tokenize(match.group(0))

	unique_tokens = set(collected_tokens)

	# This will search through the words in the dialogs and only use the words and not symbols.
	for word in set(collected_tokens):
		if re.search('[\w]+', word, re.UNICODE) == None:
			unique_tokens.remove(word)

	dialog =[(word,collected_tokens.count(word)) for word in unique_tokens]

	# This will sort the words with in "" and print the top 20 words for all of the dialogs.
	dialog_sorted = list(reversed(sorted(dialog, key=lambda tup: tup[1])))
	top_dialog = dialog_sorted[:20]
	print top_dialog


if __name__ == '__main__':
	main()
	