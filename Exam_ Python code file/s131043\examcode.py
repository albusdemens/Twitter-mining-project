#Author: Skuli Freyr Hinriksson and Asgeir Ogmundarson
#Instructions:
#Have the .txt file you wish to use in the program in the same folder as the .py file and run the following command:
#python examcode.py

def getwords(file): #function to get all the words from a specific txt file to a list
	lineslist = [] #list for all the lines in the txt file
	wordslist = [] #list for all the words in the txt file

	while 1: #loop through all the lines in the txt file
		line = file.readline() 
		if not line:
			break
		line = line.lower() #change every line to lower case
		lineslist.append(line) #put each line in the list

	for i in range(len(lineslist)): #loop through all the lines in the list
		words = lineslist[i].split() #acquire all the words in the line in a list

		for j in range(len(words)): #loop through the word list to add them to another list
			wordslist.append(words[j]) 

	return wordslist
	
def countwords(wordslist): #function to count unique words in a list
	sortedwordlist = sorted(wordslist) #sort all the words in the input list
	wordcounter = 0 #declare a word counter
	wordlistcounter = [] #declare a list for the frequency of words
	uniqewordlist = [] #declare a list for every unique word

	for i in range(len(sortedwordlist)-1): #loop through the sorted words list
		if sortedwordlist[i] != sortedwordlist[i+1]: #if the word after the current word is not the same, then add to the unique word list
			uniqewordlist.append(sortedwordlist[i])
			wordlistcounter.append(wordcounter+1)
			wordcounter = 0
		else: 
			wordcounter += 1

	if wordcounter != 0: #this is done to ensure there is no word left behind
		uniqewordlist.append(sortedwordlist[len(sortedwordlist)-1])
		wordlistcounter.append(wordcounter+1)
		wordcounter = 0

	return uniqewordlist, wordlistcounter

def printtopwords(wordlist, wordlistcounter ,number): #function to print a specific number of the most frequent words
	resultwords = [] #declare a list for the results
	for i in range(number): #find the speciffic most frequent number of words
		maxfreq = max(wordlistcounter)
		wordposition = wordlistcounter.index(maxfreq)
		maxword = wordlist[wordposition]
		resultwords.append(maxword)
		wordlist.remove(maxword)
		wordlistcounter.remove(maxfreq)

	return resultwords

if __name__ == "__main__":
	filename = raw_input("Enter the filename: ") #user specifies the filename
	no = int(raw_input("Enter how many of most frequent words are desired: "))

	file = open(filename) #the system opens the user specified filename
	wordslist = getwords(file) #get all the words out of the txt file

	[uniqewordlist, wordlistcounter] = countwords(wordslist) #get all the unique words from the file
	print printtopwords(uniqewordlist, wordlistcounter, no) #print the desired result