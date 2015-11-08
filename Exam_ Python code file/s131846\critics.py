__author__ = 'svavarm'

# IMPORTANT: To use the script, you need to install BeatifulSoup (bs4)
# You also need to use the following standard python modules: difflib, sys, argparse, requests
# This has been tested on Python 2.7.5.

# This script will search www.metacritic.com for a certain movie that is passed in through command line argument.
# It will give you a list of matches (only first page for now) and then tell you which is the closes match by measuring
# the sequences of the search query and the product id returned from metacritic.
# To get help, use: python criticts.py -h

##########
# Example:
##########

# svavarm$ python critics.py Aliens
# Searching for movie: Aliens

# Found 7 matches

# Cowboys & Aliens
# Aliens
# AVPR: Aliens vs Predator - Requiem
# Monsters vs Aliens
# Aliens in the Attic
# Aliens of the Deep
# Mutant Aliens

# Best match is: Aliens (http://www.metacritic.com/movie/aliens)


import difflib
import sys
import argparse
import requests
import bs4


class MetacriticSearchResult(object):
    def __init__(self, product_id, product_url, product_title):
        """Initializes the Metacritic search result object
        """
        self.product_id = product_id
        self.product_url = product_url
        self.product_title = product_title
        self.match_ratio = 0


class MetacriticPy(object):
    def __init__(self):
        """Initialize the Metacritic class
        """
        self.__category = None
        self.__query = None
        self.__search_best_match = None
        self.__search_results = []
        self.__base_search_url = "http://www.metacritic.com/search"

    def __get_encoded_query(self):
        """Creates and returns an encoded query string to perform the search with
        :returns: Encoded query string to perform search with
        """
        # remove _,-,: and change " " to + and create the url that metacritic understands
        encoded_query = self.__query.replace("_", "").replace("-", "").replace(":", "").replace(" ", "+")
        return encoded_query

    def __get_search_url(self):
        """Creates and returns the url that is used to perform metacritic searches
        :returns: Url
        """
        return "{}/{}/{}/results?sort=relevancy".format(self.__base_search_url, self.__category,
                                                        self.__get_encoded_query())

    @staticmethod
    def __request_page(url):
        """Requests a webpage from url
        :param url: The url to request a webpage from
        :returns: The request object
        """
        request = requests.get(url)
        return request

    @staticmethod
    def __perform_scrape(content):
        """Performs a scrape on the raw html using BeautifulSoup, creates array of results and finds the best match
        :rtype : MetacriticSearchResult[]
        :param content: The raw html content to scrape
        :returns: List of search results
        """
        # get the list of resulting objects
        soup = bs4.BeautifulSoup(content)
        results = soup.find_all("h3", {"class": "product_title"})

        scrape_results = []
        for result in results:
            # get the url
            a = result.find("a")
            if a:
                # create a result object
                product_id = a["href"][1:].replace("/", "_")
                url = "http://www.metacritic.com" + a["href"]
                product_title = a.text.strip()
                hit = MetacriticSearchResult(product_id, url, product_title)
                scrape_results.append(hit)

        return scrape_results

    def __calculate_best_match(self, search_results):
        """Calculates the match ratio for each search result, updates __search_best_match and returns the updated list
        :param search_results: The search results to calculate the best match in
        :rtype: MetacriticSearchResult[]
        :returns: Returns array updates with match ratio for each item
        """
        best_match = None
        for result in search_results:
            # calculate how close a match this is by comparing query with the product_id
            # TODO: remove the category from the product id before using difflib (faster?)
            result.match_ratio = difflib.SequenceMatcher(None, self.__query, result.product_id).ratio()

            # check if best results
            if best_match is None:
                best_match = result
            elif best_match and result.match_ratio > best_match.match_ratio:
                best_match = result

        self.__search_best_match = best_match

        return search_results

    def search(self, category, query):
        """Performs a search and eturns the best matching item by measuring the sequences of query agains ids
        :param category: The category to search in
        :param query: The search query
        :rtype: MetacriticSearchResult[]
        :returns: The best matching search result
        """
        # clear the variables
        self.__search_results = []
        self.__search_best_match = None

        self.__category = category
        self.__query = query

        # request the search page
        # TODO: Check the response status_code, will be easier to return meaningful errors
        search_url = self.__get_search_url()
        content = self.__request_page(search_url).content

        # do the content scraping
        scrape_results = self.__perform_scrape(content)

        # calculate the best match
        self.__search_results = self.__calculate_best_match(scrape_results)

        return self.__search_results

    def get_best_match(self):
        """Returns the best match from the last search
        :rtype: MetacriticSearchResult
        :returns: Best match from the last search
        """
        return self.__search_best_match


def parse_arguments():
    """Parses arguments using argparse module
    :returns: object with arguments as attributes
    """
    parser = argparse.ArgumentParser(prog="critics",
                                     description="This script gets information about movies on metacritic.com")
    parser.add_argument('movie', help="The name of the movie to search for")
    args = parser.parse_args()
    return args


def main(argv):
    """Main method
    :param argv: Command line arguments
    :return: 1 if error, 0 otherwise
    """
    # can't control how argparse returns error easily, so removed it from exception handling for now
    args = parse_arguments()

    try:
        # probably won't use anything other than movie for this project
        # but doesn't hurt to think about the future
        category = "movie"
        print "Searching for {}: {}\n".format(category, args.movie)

        # get all matches
        metacritic = MetacriticPy()
        results = metacritic.search(category, args.movie)

        # print some results
        print "Found {} matches\n".format(len(results))

        for result in results:
            print result.product_title

        best_match = metacritic.get_best_match()
        print "\n"
        print "Best match is: {} ({})".format(best_match.product_title, best_match.product_url)
    except:
        # TODO: way to broad exception catch, change later
        print sys.exc_info()
        return 1  # exit because of error
    else:
        return 0  # exit without error


if __name__ == '__main__':
    sys.exit(main(sys.argv))