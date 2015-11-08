# -*- coding: utf-8 -*-

"""
scraper API
~~~~~~~~~~~~

This module implements a http://www.meneame.net scraper

:copyright: (c) 2013 by Albert Fernandez de la Pena s112213 at student.dtu.dk
:license: Apache2

"""
import argparse
import logging
import re
import json
import os
import sys
from time import sleep
try:
	import requests
	from bs4 import BeautifulSoup
except ImportError, err:
	logging.error('Could not load module: %s' % (err))
	sys.exit(1)

MENEAME_DEFAULT_DIR = 'meneame_stories'
MENEAME_STORY_NAME = 'meneame_%s_%d.json'

# URL
MENEAME_BASE_URL = "http://www.meneame.net"
MENEAME_TOP_STORIES_URL = MENEAME_BASE_URL + "/topstories.php"

def extract_stories(text):
	"""Parses a HTML page and builds a :dict: with the
	following info: id, title, url, votes, clicks and author.
	Returns :dict:`parsed_stories` object.
	
	:param text: string with the content of a meneame web page.
	
	"""
	parsed_stories = []
	
	soup = BeautifulSoup(text)
	stories = soup.find_all('div', {'class': 'news-body'})
	for story in stories:
		# build a dict with all the relevant attributes
		meneame_story = dict()
		
		# number of votes
		id_temp = story.find('div', {'class': 'votes'})
		meneame_story['votes'] = int(id_temp.a.string)
		
		# extract the id
		id_regex = re.match('a-votes-(\d*)', id_temp.a['id'])
		if id_regex:
			meneame_story['id'] = int(id_regex.group(1))
			
		# number of clicks
		clicks_regex = r = re.match('\s*(\d*)\s.*', story.find('div', {'class': 'clics'}).string)
		if clicks_regex:
			meneame_story['clicks'] = int(clicks_regex.group(1))
		
		meneame_story['title'] = story.h2.a.string
		meneame_story['url'] = story.h2.a['href']
		
		# extract the user id
		user_a = story.find('a', {'class': 'tooltip'})
		user_regex = re.match('\/user\/(.*)', user_a['href'])
		if user_regex:
			meneame_story['author'] = user_regex.group(1)
		
		parsed_stories.append(meneame_story)
	return parsed_stories
		
def scrap_stories(base_url, time_range, page_start, page_end, output_dir, overwrite, pause):
	"""Recursively requests stories to the url specified
	
	:param base_url: URL of meneame news
	:param time_range: Time range from which to parse news (the top news between the following '24h', '48h', 'week', 'month',
		'year', 'all'
	:param page_start: number of page from where start scraping
	:param page_end: number of page to stop
	:param output_dir: directory where the parsed stories are stored
	:param overwrite: if ``True``, already scraped stories will be scraped again
	:param pause: define a time pause between each request
	"""
	current_page = page_start
	no_more_pages = False
		
	while current_page != page_end and not no_more_pages:
		
		current_page_path = os.path.join(output_dir, MENEAME_STORY_NAME
			% (time_range, current_page))
		
		if not os.path.exists(current_page_path) or overwrite:
			logging.info('Scraping page %d ...' % current_page)
			try:
				params = {'page': current_page, 'range': time_range}
				r = requests.get(base_url, params=params)
				
				# parse web page, and store it to file
				stories = extract_stories(r.text)
				if not stories:
					logging.info('no more stories')
					no_more_pages = True
				else:
					with open(current_page_path, 'w') as output_file:
						root = {'stories': stories}
						logging.info('storing %d news to file %s' % (len(stories),
							current_page_path))
						json.dump(root, output_file)
				
			except requests.exceptions.RequestException as e:
				# could be a Timeout, TooManyRedirects, no internet...
				logging.error('could not scrap page %s. Skiping ...' % current_page)
			
		else:
			logging.info('Page %d already scrapped ...' % current_page)
			
		current_page += 1
		sleep(pause) # delay for the specified number of seconds
		

def main():
	
	parser = argparse.ArgumentParser(description='Scrap meneame.net stories')
	parser.add_argument('-t', '--time', choices=['24h', '48h', 'week', 'month',
		'year', 'all'], default='year', help='the timeframe to download')
	parser.add_argument('-s', '--start', type=int, default=1, 
		help='the page to start with')
	parser.add_argument('-o', '--output', default=MENEAME_DEFAULT_DIR,
		help='the output directory where the stories will be stored. Default ./%s'
			% (MENEAME_DEFAULT_DIR))
	parser.add_argument('-m', '--max', type=int, default=100000, 
		help='the number of the last page to scrap')
	parser.add_argument('-p', '--pause', type=int, default=0, 
		help='define a timer between requests (in seconds)')
	parser.add_argument('--overwrite', action='store_true',
		help='overwrite already downloaded stories')
	parser.add_argument('--verbose', action='store_true', 
		help='print debugging info')
	parser.add_argument('--version', action='version', 
		version='%(prog)s 1.0')
		
	args = parser.parse_args()
	
	# turn on logging
	if args.verbose:
		logging.basicConfig(level=logging.INFO,
			format='%(asctime)s %(levelname)-8s %(message)s',)
	
	# transform the time range string into it's corresponding id
	time_range = ['24h', '48h', 'week', 'month', 'year', 
					'all'].index(args.time)
					
	# create output directory if does not exist
	if not os.path.exists(args.output):
		os.makedirs(args.output)
	
	scrap_stories(MENEAME_TOP_STORIES_URL, time_range, args.start, args.max,
				args.output, args.overwrite, args.pause)
	
		
if __name__ == '__main__':
	main()