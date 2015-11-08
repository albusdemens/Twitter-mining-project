#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Weather Advisor Module

"""

__version__ = 0.1
__author__ = "Woody Rousseau"
__all__ = ["WeatherAdvisor"]

import simplejson as json
from urllib2 import Request, urlopen, URLError, HTTPError
import random
import math

class WeatherAdvisor:
	"""
	Weather Advisor module

	This module will give you weather information from your current location, and will specify which nearby cities you should go to
	in order to experience better weather or temperature. Careful though, because the city might not be interesting to visit !

	The free API used to get the weather information is http://http://openweathermap.org/
	In order not to overload its server, please do not use this program excessively. The program might not find a proper advice,
	because the number of requests are limited in order to find nearby cities.

	>>> paris = WeatherAdvisor('Paris')
	>>> paris.displayWeather()
	scattered clouds

	>>> paris.displayTemperature()
	16.95°C

	>>> paris.whereToGo('temperature')
	The weather description in Paris is "scattered clouds" and the temperature is 16.95°C
	You should go to Onnaing where the weather description is "few clouds" and the temperature is 18.14°C

	>>> paris.whereToGo('weather')
	The weather description in Paris is "scattered clouds" and the temperature is 16.95°C
	You should go to Frelinghien where the weather description is "Sky is Clear" and the temperature is 14°C
	"""

	"""
	Weather condition codes are numerous and listed on http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes
	Only 9 weather descriptions are used and rated from 0 to 8 (0 being the worst weather, 8 being the best). 
	This is done in weatherDict, a static variable which associates each weather "icon" to the score of this weather, both for day and night.
	""" 
	weatherDict = { '13d' : 0, '11d' : 1, '09d' : 2, '10d' : 3, '50d' : 4, '04d' : 5, '03d' : 6, '02d' : 7, '01d' : 8, '13n' : 0, '11n' : 1, '09n' : 2, '10n' : 3, '50n' : 4, '04n' : 5, '03n' : 6, '02n' : 7, '01n' : 8}
	
	def __init__(self, cityName):
		"""
		Constructs the WeatherAdvisor structure with the name of the current city as the input. It loads the json data from the API.

		"""
		self.cityName = cityName.title()
		request = Request('http://api.openweathermap.org/data/2.5/weather?q='+cityName+'&units=metric')
		try: 
			response = urlopen(request)
		except HTTPError, e:
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code
		except URLError, e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		else:
			self.currentCityData = json.load(response)

	def displayWeather(self):
		"""
		Prints the current city weather description.
		
		"""
		print self.currentCityData['weather'][0]['description']

	def displayTemperature(self):
		"""
		Prints the current city temperature in Celsius degrees.
		
		"""
		print str(self.currentCityData['main']['temp']) + '°C'

	def whereToGo(self, mode):
		"""
		Find a better city to go to, either weather wise, or temperature wise, depending of the chosen mode.
		In order not to overload the API server, 10 tries will be made.
		For each try, random latitude and longitude are randomly computed, so that :
		(targetLat-sourceLat)^2+(targetLon-sourceLon)^2 = 4.0

		The request might fail, because of :
		- The limited number of tries
		- In weather mode, weather might not change that much in wide areas
		
		"""
		found = False
		tries = 0
		while(tries < 10 and not(found)):
			newLat = random.uniform(0,2)
			newLon = random.choice([-1,1])*math.sqrt(4-newLat*newLat)
			newLat = self.currentCityData['coord']['lat'] + newLat
			newLon = self.currentCityData['coord']['lon'] + newLon
			request = Request('http://api.openweathermap.org/data/2.5/find?lat='+str(newLat)+'&lon='+str(newLon)+'&cnt=1&units=metric')
			try: 
				response = urlopen(request)
			except HTTPError, e:
				print 'The server couldn\'t fulfill the request.'
				print 'Error code: ', e.code
			except URLError, e:
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			else:
				nearbyCity = json.load(response)['list'][0]
				if (mode == 'weather') and (self.weatherDict[nearbyCity['weather'][0]['icon']] > self.weatherDict[self.currentCityData['weather'][0]['icon']]):
					weatherChoice = nearbyCity
					found = True
				elif (mode == 'temperature') and (nearbyCity['main']['temp'] > self.currentCityData['main']['temp']):
					weatherChoice = nearbyCity
					found = True
			tries = tries + 1
		if (not(found)):
			print 'No proper location was found. This is most likely to happen if you picked the "weather" mode.'
			return
		print 'The weather description in ' + self.cityName + ' is "' + self.currentCityData['weather'][0]['description'] + '" and the temperature is ' + str(self.currentCityData['main']['temp']) + '°C'
		print 'You should go to '+weatherChoice['name'] + ' where the weather description is "' + weatherChoice['weather'][0]['description'] + '" and the temperature is ' + str(weatherChoice['main']['temp']) + '°C'

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		cityName = 'Copenhagen'
	else:
		cityName = sys.argv[1]
	wa = WeatherAdvisor(cityName)
	wa.whereToGo('temperature')
