#!/usr/bin/env python
from HTMLParser import HTMLParser
from pprint import pprint as pr
import re

##
# "Generic" SAX-styled HTML-parser
# Idea is that you can feed the parser some information, 
# which makes it aware of what information it is supposed to look for as well as to what to return it as.
# As this parser only iterates over the HTML once, it "SHOULD" be faster than using Beautifulsoup, but this is untested.
#
# Current expected way for parsing pattern:
#{
#						'tag': {
#							'target_name':'TARGETNAME',
#							'attributes' : [('ATTRIBUTENAME', 'ATTRIBUTEVALUE'),],
#							'multiple_return_values':True,
#							'type':'data',
#							'subtags':None,
#						},
#					}
#
#
# v. 0.0.1
# By Rune Thor Maartensson s093475
# TODO: 
# - Sphinx documentation
# - Improve generalization, it has only been tested on a very limited dataset
# - Implement code to properly handle nesting, example a generic p tag in another p tag, where the second is wanted, without other id.
##
class sax_style_HTML_Parser(HTMLParser):

	def __init__(self, parsing_pattern):
		self.__result = {}
		self.__parsing_pattern = parsing_pattern
		self.__tag_stack = []
		self.__current_tag = ''
		self.__getdata = False
		HTMLParser.__init__(self)

	# Parse the contents of a file or file-like object
	def parse(self, file_reference):
		# Overridden for example purposes!
		#self.feed(file_reference.read())
		self.feed(file_reference)
		return self.__result

	# Overridden method from HTMLParser, handles start of tags
	def handle_starttag(self, tag, attrs):
		# Get information about the tag if possible
		tag_details = self.get_tag_details(tag)

		if tag_details is not None:
			# if the tag has the attributes we are looking for, select is as current tag, and add it to the tag_stack
			if attrs[0] in tag_details['attributes']:
				self.__tag_stack.append((tag, 1))
				self.__current_tag = tag
				if tag_details['type'] == 'data':
					self.__getdata = True
			# If the tag is the same, but the attributes are different, increment the tag_stack value for the last tag (should)
			elif tag == self.__current_tag:
				tag_info = self.__tag_stack.pop()
				self.__tag_stack.append((tag, tag_info[1] + 1))
	
	# Overridden method from HTMLParser, handles ends of tags
	def handle_endtag(self, tag):
		# if the tag is the one we are looking for, decrement counter
		if tag == self.__current_tag:
			tag_info = self.__tag_stack.pop()
			tag_count = tag_info[1] - 1
			if tag_count == 0:
				self.__current_tag = ''
	
	# Overridden method from HTMLParser, handles data and saves it to the result
	def handle_data(self, data):
		if self.__getdata:
			tag_details = self.get_tag_details(self.__current_tag)
			target_name = tag_details['target_name']
			multiple_return_values = tag_details['multiple_return_values']
			# if multiple values of this type is expected, use a list
			if multiple_return_values:
				try:
					self.__result[target_name].append(data)
				except KeyError, e:
					self.__result[target_name] = []
					self.__result[target_name].append(data)
			else:
				self.__result[target_name] = data
			self.__getdata = False

	# Method used to get tag details information, in a contained way.
	def get_tag_details(self, tag):
		try:
			return self.__parsing_pattern[tag]
		except KeyError:
			return None


# Example data
parsing_pattern = 	{
						'p': {
							'target_name':'test',
							'attributes' : [('class', 'test'),],
							'multiple_return_values':True,
							'type':'data',
							'subtags':None,
						},
					}

test_parser = sax_style_HTML_Parser(parsing_pattern)
result = test_parser.parse("<!DOCTYPE html><html><a hmm='kage'>hej</a><p class='test'>test</p><b>hmm</b><p class='test'>Test 200</p></html>")
pr(result)