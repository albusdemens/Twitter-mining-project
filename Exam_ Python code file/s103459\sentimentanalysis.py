# This program is used to perform simple sentiment analysis of strings

import nltk

teststring = "The movie is very bad, I barely like it. It is not horrible, though."

def sentimentanalysis(s):
    # The nltk (natural language toolkit) library is used to isolate words
    words = nltk.word_tokenize(s)
    
    # Test-sized dictionaries of positive/negative word and their value
    negatives = {'hate': 3, 'bad': 3, 'horrible': 3}
    positives = {'like': 3}
    
    # Words used to increase or decrease the value of a sentiment
    incrementers = ['very','too']
    decrementers = ['barely']
    
    # Words that invert the sentiment of another word
    inverters = ['not','doesn\'t']
    
    # Variables are initialized
    sentimentval = 0
    previousword = ''
    
    # Each word is checked for a postive or negative sentiment
    # Previous words are checked to see if they modify the value 
    for word in words:
        
        if negatives.has_key(word):
            wordvalue = negatives.get(word)
            if incrementers.__contains__(previousword):
                wordvalue += 1
            elif decrementers.__contains__(previousword):
                wordvalue -= 1
            
            if inverters.__contains__(previousword):
                sentimentval += wordvalue
            else:
                sentimentval -= wordvalue
        
        elif positives.has_key(word):
            wordvalue = positives.get(word)
            if incrementers.__contains__(previousword):
                wordvalue += 1
            elif decrementers.__contains__(previousword):
                wordvalue -= 1
            
            if inverters.__contains__(previousword):
                sentimentval -= wordvalue
            else:
                sentimentval += wordvalue
        
        previousword = word
        
    return sentimentval

# The teststring is evaluated and printed
value = sentimentanalysis(teststring)
if value > 0:
    print("String has positive sentiment (value = " + value + ").")
elif value > 0:
    print("String has negative sentiment (value = " + value + ").")
else:
    print("String has neutral sentiment (value = 0).")