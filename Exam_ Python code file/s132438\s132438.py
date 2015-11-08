import urllib2
import re
import nltk # install nltk - see the link: http://nltk.org/install.html
def main():
	print("Jennifers code - starting point")
	#fetching URL by using urllib2
	response = urllib2.urlopen('http://www.gutenberg.org/cache/epub/3289/pg3289.txt')
	html = response.read() # reading it from an object(response) to a string(html)
	match = re.search('(p|P)roduced [\-\.\,\w ]+', html) # returns a match object, regex is used for pattern matching that match the text
	match2 = re.search('\*\*\*\ END OF THIS PROJECT GUTENBERG EBOOK',html)
	#By applying \w it will cut of letter by letter but applying [\w]+ it will take te whole word, http://www.gskinner.com/RegExr/
	print match
	txt = html[match.end():match2.start()] # takes the html text to its end - match.end 
	
	top_words(txt)

def top_words(txt):
	"""
	Divide the text string into word sequence
	"""
	tokens = nltk.word_tokenize(txt)
	"""
	set function is used in tokens so it only takes the unique words
	and gives it counts according to how many time it appears in the text
	"""
	my_list = list()
	for token in set(tokens):
		my_list.append((token, tokens.count(token))) #add a new list called token count
	"""
	it sort the the unique words, reverse it so it it at numerical order and puts it in a new list
	"""
	my_list = list(reversed(sorted(my_list, key=lambda tup: tup[1]))) # tup = list
	#print len(din_list) # finding the length of the words 

	print "Top 50 - With symbols"
	print my_list[:50]

	
	for token in list(my_list): #creates a new list from  my_list

	"""
	If its true it will return a match object if not it will return None - 0 beacuse it takes the word and not it count
	"""
		if re.search('[\w]+', token[0]) == None:
			#remove the tokens which does not match the regex
			my_list.remove(token)

	print "Top 50 - Without symbols"
	print my_list[:50]

if __name__ == "__main__": 
	main()