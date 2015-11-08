# Created by:	Georgios Chatzigeorgakidis
# Student No:	s121078
####################### TEXT MOOD CALCULATOR USING THE AFINN CORPORA ############################
import requests
import zipfile
import StringIO
import re
import counter
import matplotlib.pyplot as plt

######################### Class to compute a text's mood ###################################
class hedonometer:
    def __init__(self):
        print "Hedonometer object initiated..."
        
	# The HEDONOMETER algorithm, source:
    # http://www.plosone.org/article/info:doi/10.1371/journal.pone.0026752
    def compute_mood(self, cnt, mood_list):		
	
		# Get the words that also exist in AFINN
        word_bag = [key for key in cnt]
        final_word_bag = [] 
        for word in word_bag:
            if mood_list.has_key(word): final_word_bag.append(word)
		
		# Compute the total frequency of the text's words
        total_freq = 0;    
        for word in final_word_bag:
            total_freq += float(cnt[word])
		
		# Compute the relevant frequency for every word in the text
        rel_freq = []
        for word in final_word_bag:
            rel_freq.append(cnt[word]/total_freq)
        
		# Compute the final mood of the text
        mood = 0
        count = 0
        for word in final_word_bag:
            if mood_list.has_key(word):
                mood += float(mood_list[word])*rel_freq[count]
                count += 1
        return mood, final_word_bag
        
	# Calculate the word frequencies of a given text 
    def count_words(self, text):
        # Create a word bag ignoring punctuation
        word_bag = re.findall(r"[\w']+|[.,!?;]", text) 
        # Count the word occurrences of the comments for each date
        uni_word_bag = [unicode(word, 'utf-8') for word in word_bag] # Convert to unicode              
        cnt = counter.Counter(uni_word_bag)
        return cnt

######################################### Main Program ##############################################
# Get the AFINN corpora
remotefile = requests.get('http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip').content
imm6010 = zipfile.ZipFile(StringIO.StringIO(remotefile)).open('AFINN/AFINN-111.txt').readlines()

#Create a dictionary with the extracted words' moods
moods = {}
for string in imm6010:
    moods[re.split(r'\t', string)[0]] = re.split(r'\t', string)[1]

# Sample text that uses several words from the AFINN word corpora
text = "The explorations begun due to the ability of the adventurous but arrogant and at the same \
        time awesome people. They sentenced the unbelievable serene to 10 sorrowful years in prison. \
        they were the winners! Unbelievable sorrowful serene!"

# Instantiate the hedonometer class
text = text.lower()
hedon = hedonometer()

# Count and get the moods of the sample text and the whole AFINN corpora
counted_words = hedon.count_words(text)
corpora_words = [key for key in moods]
corpora_text = ' '.join(corpora_words)
counted_corpora_words = hedon.count_words(corpora_text)
sample_text_mood, sample_text_words = hedon.compute_mood(counted_words, moods)
corpora_mood, corpora_words = hedon.compute_mood(counted_corpora_words, moods)

# Old string formatting
print "The mood for the given text is: %(number)5.10f" % {"number" : sample_text_mood}
# New string formatting
print "The mood for the whole AFINN corpora is: " + str(corpora_mood)

# Plot showing the moods for the sample text's words
plt.figure(1)
plt.plot([moods[w] for w in [word for word in sample_text_words]])
plt.xticks(range(len(sample_text_words)), sample_text_words, rotation='vertical')
plt.xlabel("Words(in appearing sequence)")
plt.ylabel("Mood")
plt.title("Sample text's words mood plot")

# Plot showing the moods for the corpora's words
plt.figure(2)
plt.plot([moods[w] for w in [word for word in corpora_words]])
plt.xlabel("Words(in appearing sequence)")
plt.ylabel("Mood")
plt.title("Corpora's words mood plot")
plt.show()