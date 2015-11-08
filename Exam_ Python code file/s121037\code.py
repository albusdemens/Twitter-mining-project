'''
Created on 30 Sept, 2013

@author: Ruxandra Nistor

'''

import urllib2
import urllib
import re


# The type variables are used by the PlaceFinder factory to generate objects depending
# on the data source.
# For this partial implementation, only Wikitravel will be used a source
WIKITRAVEL_TYPE = "Wikitravel_type"


class Place(object):
	"""
	Class that represents a specific place/attraction
	It contains a tag and a name; more fields might be a added
	"""
	tag = ""
	name = ""
	def __repr__(self):
		#overridden to print the tag and the name
		if self.tag != None:
			return (self.tag + " : " + self.name)
		return ("No_tag : " + self.name)
	def __str__(self):
		#overridden to print the tag and the name
		if self.tag != None:
			return (self.tag + " : " + self.name)
		return ("No_tag : " + self.name)
	
class PlaceFinder(object):
	'''
	Class that contains genereal method for finding places, independent of the 
	data source
	'''
	def factory(type, city_name):
		"""
		Static method that creates objects that inherit from PlaceFinder depending on the 
		type sent as a parameter
		"""
		if(type == WIKITRAVEL_TYPE): return WikitravelPlaceFinder(city_name)
		assert 0, "Incorrect Place Finder type" + type
	factory = staticmethod(factory)
	
	def __init__(self, city_name):
		"""
		Constructor that receives the city name and also initialises the urllib2 opener
		"""
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		self.city_name = city_name
	
	def getPage(self):
		"""
		Method that returns the content of a page in a utf-8 encoded format.
		
		It uses the data source and the city_name to determine the url.
		"""
		opener = self.opener
		url = self.base_url + self.city_name + self.end_url
		print "Fetching data from: "+ url
		print "..."
		infile = opener.open(url)
		page = infile.read()
		ucontent = unicode(page, encoding="utf-8")
		ucontent = ucontent.encode(encoding="utf-8")
		return ucontent

	def getPlaces(self):
		"""
		Method returns a list of Place objects from the data sources
		"""
		return []
			
	
class WikitravelPlaceFinder(PlaceFinder):

	def __init__(self, city_name):
		"""
		Constructor that sets up the data source based on the city name
		"""
		super(WikitravelPlaceFinder, self).__init__(city_name)
		self.base_url = "http://wikitravel.org/wiki/en/api.php?format=txt&action=query&format=txt&titles="
		self.end_url= "&prop=revisions&rvprop=content"
		self.places = []
		
	def getPlaces(self):
		"""
		Method returns a list of Place objects from wikitravel
		"""
		if len(self.places) > 0:
			return self.places
		page = self.getPage()
		
		check_redirect = re.findall("#REDIRECT \[\[(.*)\]\]", page, re.UNICODE)
		
		#If the page contains #REDIRECT then follow the redirect.
		if len(check_redirect) > 0:
			print "Redirecting to: " + check_redirect[0]
			self.city_name = check_redirect[0] #urllib.urlencode(, encoding='utf-8')
			page = self.getPage()
			
		
		start_tag = "== ?See ?=="
		end_tag = "== ?Do ?=="
		pattern = start_tag + ".*" + end_tag
		
		#search in between See and Doo
		see_text = re.findall(pattern, page, re.UNICODE|re.DOTALL)[0]
		#find the headers (tags)
		tags = re.findall(r'===[^=]*===', see_text, re.UNICODE|re.DOTALL)
		tags.insert(len(tags), end_tag)
		
		#search for places in every tag
		for i in range(0, len(tags) - 1):
			tag = tags[i]
			pattern =  tags[i] + ".*" + tags[i + 1]
			tagged_text = re.findall(pattern, see_text, re.UNICODE|re.DOTALL)
			
			#if there is no text for the current tag, continue to the next one
			if len(tagged_text) > 0: tagged_text = tagged_text[0]
			else: continue
			
			#retrieve the places that are in between three quotes
			place_pattern = "\'\'\'([\n\s\w\d\b\(\).]*)\'\'\'"
			places = re.findall(place_pattern, tagged_text, re.UNICODE|re.DOTALL)
			
			#retrieve the places that are tagged with <see>
			place_pattern = "<see name=\"([^\"]*)\""
			places.extend(re.findall(place_pattern, tagged_text, re.UNICODE|re.DOTALL))
			
			#add all the places that have a tag in the place list
			for text in places:
				if(tag != None):
					p = Place()
					p.tag = tag[3:len(tag)-3].strip()
					p.name = text.strip()
					self.places.append(p)
					
		return self.places
		
#tested with Copenhagen, Bucharest, Berlin, Rome, Paris, Warsaw, Riga, Tallinn
finder = PlaceFinder.factory(WIKITRAVEL_TYPE, "Tallin")
places = finder.getPlaces()
for place in places:
	print place



