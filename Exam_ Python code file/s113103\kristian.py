#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from collections import OrderedDict
import urllib2
import re
import nltk
import nltk.data

def AUTHOR_A_BOOKS():
	"""
	Pseudo constant, that returns the URL for the book to download
	"""
	return {"Bog A": "http://www.gutenberg.org/cache/epub/2852/pg2852.txt" }

def main():
	print "Welcome to the program written by"
	print "  Kristian Dam-Jensen, S113103"
	print "================================="
	author_a_books = {}
	for title,url in AUTHOR_A_BOOKS().items():
		author_a_books[title] = stylometric_coordinate(
			clean_gutenberg_extra(
			urllib2
			.urlopen(url)
			.read()))
	for title, style in author_a_books.items():
		print "TITLE: {0}".format(title)
		for data in style:
			print "{0}\t:\t{1}".format(data[0],data[1])

def stylometric_coordinate(text):
	style = []
	style.append(("disparity", word_disparity(text)))
	wpc = average_words_per_sentence(text)
	style.append(("mean wpc", wpc["mean"]))
	style.append(("median wpc", wpc["median"]))
	for n in range(1,11):
		style.append(("{0}-char words".format(n), wordlength_frequency(text,n)))
	return style

def word_disparity(text):
	return len(set(tokenize(text)))

def wordlength_frequency(text,word_length):
	words = tokenize(text)
	return sum(1 for w in words if len(w) == word_length)

def average_words_per_sentence(text):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(text)
	average_words = [len(tokenize(sentence)) for sentence in sentences]
	output = {}
	output["mean"] = sum(average_words)/len(average_words)
	output["median"] = sorted(average_words)[len(average_words)//2]
	return output

def clean_gutenberg_extra(text):
	"""
	Returns string with Project Gutenberg pre and after -text
	Uses regex to match the beginning and end of the text, since Project Gutenberg
	files include a lot of legalese.
	"""
	regex_string_start = '\*\*\* START OF THIS PROJECT GUTENBERG EBOOK[\S ]+'
	start_match = re.search(regex_string_start, text, re.UNICODE)
	start_index = start_match.end()

	regex_string_end = '\*\*\* END OF THIS PROJECT GUTENBERG EBOOK [\S ]+'
	end_match = re.search(regex_string_end, text)
	end_index = end_match.start()
	text = text[start_index:end_index].strip()
	return text

def remove_values_from_list(list,unwanted_values):
	"""
	Returns a new list where all values have been checked that they are not
	present in the unwated_values list.
	"""
	return [x for x in list if x not in unwanted_values]

def tokenize(text):
	"""
	Extension of nltk's tokenize, that removes unwated values, and lowercases
	"""
	words = nltk.word_tokenize(text)
	words = remove_values_from_list(words,[",","''"])
	return words

if __name__ == '__main__':
	main()
