# -*- coding: utf-8 -*-

"""
LikeTextAnalysis.py

Uses nltk, regular expressions and AFINN to get some insights on the provided
texts which eventually should be Facebook posts.

This is done to find patterns in when a post get the thump up by other users.

Additional ideas could be to include:
Time of post
Number of comments
Type of post, with e.g. picture, video.
Make a test post from our evaluation to see if we get the expected posts.

"""

__version__ = 0.01
__author__ = "Louis Flyvholm"

import nltk
import re
import math
import numpy as np
import matplotlib.pyplot as plt

def text_calculations(input_text, fb_name):
    """
    Uses nltk to tokenize and convert to nltk text.
    
    Uses nltk functions and regular expressions to extract information of the
    input text in the forms:
        -Number of words
        -Number of unique Words
        -Number of characters in the text
        -Number of characters in the words (without whitespaces)
        -Average number of characters in the words
        -Number of signs
        -Number of instances of multiple signs
        -if text contains questions
        -if text contains exclamations
        -if text contain the users Facebook name 
        
    The function returns a dict:
    
    >>> '%s' % text_calculations("My sample text.", "Louis" )
    "{'exclamation': 0, 'name': 0, 'question': 0, 'multiple_signs': 0, 'number_words': 4, 'average_character_length': 3.25, 'signs': 1}"
    """
    
    token_text = nltk.word_tokenize(input_text)
    #print(token_text)
    nltk_text = nltk.Text(token_text)
    #print(nltk_text)
    
    #The number of words incl. numbers and signs.
    number_words = len(token_text)
    #print("number_words: %i" % (number_words))  
    
    #The number of unique words. 
    unique_words = len(set([each_word.lower() for each_word in nltk_text if each_word.isalpha()]))
    #print("unique_words: %i" % (unique_words))
    
    #The number of characters (including whitespaces) in all words (incl. numbers and signs)
    characters_text = len(input_text)
    #print("characters_text: %i" % (characters_text))
    
    #The number of characters (without whitespaces) in all words (incl. numbers and signs)
    characters_words = sum([len(each_word) for each_word in nltk_text])
    #print("characters_words: %i" % (characters_words))
    
    #The average number of characters in a word in this text.
    average_character_length = float(characters_words) / number_words
    #print("average_character_length: %0.2f" % (average_character_length))
    
    #number of signs
    signs = re.findall(r'[^\w\s]', input_text) # [not,( Any whitespace character, Any alphanumeric character)]
    #print(signs)
    #print("len(signs): %i" % len(signs))
    
    #number of instances of multiple following signs - could be smileys, !!!!!
    multiple_signs = re.findall(r'[^\w\s]{2,}', input_text) # At least 2 repeats of signs.
    #print(multiple_signs)
    #print("len(multiple_signs): %i" % len(multiple_signs))
    
    #If text contains questions based on "?"
    contain_question = re.findall(r'[?]', input_text)
    #print("len(contain_question): %i" % len(contain_question))
    
    #if it contains statements based on "!"
    contain_exclamation = re.findall(r'[!]', input_text)
    #print("len(contain_exclamation): %i" % len(contain_exclamation))
    
    #If the text contain the users name   
    contain_user_name = re.findall('%s'%fb_name, input_text)
    #print("len(contain_user_name): %i" % len(contain_user_name))
    
    return {'number_words':number_words, 
    'average_character_length':average_character_length, 
    'signs':len(signs), 'multiple_signs':len(multiple_signs), 
    'question':len(contain_question), 'exclamation':len(contain_exclamation), 
    'name':len(contain_user_name) }
 

def mood_calculations(input_text):
    """
    Based on code from Finn Årup Nielsen: i.a from 
    http://finnaarupnielsen.wordpress.com/2011/06/20/simplest-sentiment-analysis-in-python-with-af/ 
    
    Try to read the 'AFINN/AFINN-111.txt' file from local directory, 
    otherwise downloads and unzip the file.
    Makes call to the sentiment function on the rawText put into the function.
    
    Returns a list with the mood score and the text analysed:
    >>> '%.2f' % mood_calculations("My fun sample text.") 
    '1.79'
    """
    try:
        # AFINN-111 is as of June 2011 the most recent version of AFINN
        filename_afinn = 'AFINN/AFINN-111.txt'
        afinn = dict(map(lambda (w, s): (w, int(s)), [ 
                ws.strip().split('\t') for ws in open(filename_afinn) ]))
        #print("AFINN from local file")
        mood_score = (sentiment(input_text, afinn), input_text)
        #print("Mood score: %0.2f, text: %s" % mood_score)
    
    except IOError:
        try:
            import zipfile, requests, StringIO
            url = "http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip"
            lines = [ line.split('\t') for line in zipfile.ZipFile(StringIO.StringIO(requests.get(url).content)).open('AFINN/AFINN-111.txt').readlines() ]
            afinn = dict(map(lambda (s, v): (unicode(s, 'utf-8'), int(v)), lines))
            #print("AFINN from downloaded zip file")
            mood_score = (sentiment(input_text, afinn), input_text)
            #print("Mood score: %0.2f, text: %s" % mood_score)
        except Warning:
            print("Please ensure you have acces to the internet!")
            
    return mood_score[0]
    

def sentiment(input_text, afinn):
    """
    Code from http://finnaarupnielsen.wordpress.com/2011/06/20/simplest-sentiment-analysis-in-python-with-af/ 
        
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    # Word splitter pattern
    pattern_split = re.compile(r"\W+")
    
    words = pattern_split.split(input_text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiments = float(sum(sentiments))/math.sqrt(len(sentiments))
        
    else:
        sentiments = 0
    return sentiments
    
def plot_results(t_val, mood):
    """
    Creates a polar bar plot of the input values.
    
    """
    N = 8
    theta = np.linspace(0.0, 2 * np.pi , N, endpoint=False)
    the_stats = [t_val['number_words'], t_val['average_character_length'], 
                 t_val['signs'], t_val['multiple_signs'], t_val['question'],
                 t_val['exclamation'], t_val['name'], mood] 
    
    width = np.pi / N 

    plt.figure()
    
    handle = plt.subplot(111, polar=True)
    handle.set_xticklabels(['Word', 'AvrChar', 'Signs', '2Signs', '?', '!', 'name', 'mood'])
    
    handle.bar(theta, the_stats, width=width, bottom=1.0)
        
    plt.show()
    
  
#The texts are stored in a dict with the number of likes as values.  
TEXTS = {
"1 Within, 223 and Louisiana ??? progam. Louis This new great wonderful!" : 4,
"some other 1337 text without a bad and short name :-)" : 0,
"I just bought my first house with my wife Sarah!!!!!" : 12,  
"who stole my old bike? Bastards!" : 0
}

#query to get user name by keyboard input.
USER_NAME = raw_input('Please type your Facebook name and hit return:')


for (rawText, likes) in TEXTS.items():
    if likes > 0:
        text_c = text_calculations(rawText, USER_NAME)
        mood_v = mood_calculations(rawText)
        plot_results(text_c, mood_v)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


