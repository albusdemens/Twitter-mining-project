"""
Fetch news related to stocks.

At the moment Google Finance is the
only source supported, but soon also tweets will be supported. And maybe more
sources will be suported in the future.

Arguments:
short_name    -- (string) the short name of the stock (e.g. 'GOOG')
start_date    -- (string formatted as %Y-%m-%d) the start date
                 - articles published on this date will be included
end_date      -- (string formatted as %Y-%m-%d) the end date
                 - articles published on this date will NOT be included
order_by_date -- (boolean) whether to sort the articles by date or by relevance
                 - the default value is False

Example of how to get the most relevant Google Finance articles
related to the LinkedIn stock (LNKD) between the 15th of august and the 15th of
september 2013:

>>> articles = get_google_finance_articles('LNKD', '2013-08-15', '2013-09-15')
>>> len(articles)
58
>>> most_relevant_article = articles[0]
>>> least_relevant_article = articles[-1]
>>> most_relevant_article['relevance']
1
>>> least_relevant_article['relevance']
58
>>> most_relevant_article['title']
u'Linkedin Corp (LNKD): Could Linkedin Substitute A Recruitment Agency?'
>>> most_relevant_article['content'][:20]
'Linkedin Corp (LNKD)'

Example of how to get the earliest and the latest Google Finance article
related to the same stock and within the same time frame as above:

>>> articles = get_google_finance_articles('LNKD', '2013-08-15', '2013-09-15',
...                                        True)
>>> len(articles)
58
>>> earliest_article = articles[0]
>>> latest_article = articles[-1]
>>> import time
>>> time.strftime("%d %b %Y %H:%M:%S", earliest_article['datetime'])
'03 Sep 2013 12:13:00'
>>> time.strftime("%d %b %Y %H:%M:%S", latest_article['datetime'])
'14 Sep 2013 21:08:17'

"""
from threading import Thread
from collections import Counter
from operator import itemgetter
import urllib
import urllib2

import feedparser
import nltk

USER_AGENT = 'StockNewsCrawler/1.0 Technical University of Denmark, ' \
             '02820 Data Mining using Python, ' \
             'by: s082940 Helge Jacobsen & s110848 Magdalena Furman'
             

def get_google_finance_articles(
                                short_name,
                                start_date,
                                end_date,
                                order_by_date=False,
                               ):
    """
    Return a sorted list of dictionaries representing articles.
    
    Each dictionary represents an article and has the following keys:
    - 'datetime'
    - 'title'
    - 'wordcounts'
    - 'link'
    - 'relevance'
    - 'content'
    
    By default the list is sorted according to relevance (defined by Google
    Finance), but can be sorted by date if preferred.
    
    """
    # Initializing variables
    article_list = []

    # Fetch feed and store 'datetime', 'title', 'link' and 'relevance'
    feed_items = _get_google_finance_feed(short_name, start_date, end_date)
    for index, item in enumerate(feed_items):
        article = {}
        article['datetime'] = item['published_parsed']
        article['title'] = item['title']    
        article['link'] = item['link']
        article['relevance'] = index + 1
        article_list.append(article)
    
    # Fetch articles in parallel
    print "Fetching %s articles online" % len(article_list)
    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", USER_AGENT)]
    def fetch_online(article):
        """
        Fetch online content.
        
        Request the url for an article dictionary (article['link']) and store
        the content within this dictionary (article['content']).
        
        """
        try:
            raw_html = opener.open(article['link']).read()
            article['raw_html'] = raw_html            
            article['content'] = nltk.clean_html(raw_html)
            print '.',
        except urllib2.URLError:
            article['content'] = ''
            print 'x',
    threads = [Thread(target=fetch_online, args = (article,))
               for article in article_list] # takes tuple as args
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print '' # newline
        
    # Count words and store 'wordcounts' in dictionary
    for article in article_list:
        # Concatenate titles and content
        text = article['title'].encode('utf8') + article['content']
        # Normalize (tokenize, lowercase, stem, remove stopwords)
        word_list = _word_normalization(text)
        # Count words
        article['wordcounts'] = Counter(word_list)

    # Order by date instead of relavance if requested
    if order_by_date:
        article_list = sorted(article_list, key=itemgetter('datetime'))
    
    return article_list


# PRIVATE METHODS
# ---------------

def _get_google_finance_feed(short_name, start_date, end_date):
    """Return a list of feedparser items sorted by relevance."""
    
    # Setup URL parameters
    args = {}
    args['q'] = short_name
    args['output'] = 'rss'
    args['startdate'] = start_date
    args['enddate'] = end_date
    args['start'] = 0 # pagination (start from item number <'start'> ...)
    args['num'] = 100 # pagination (... and show the next <'num'> items.)

    # Initialize variables
    reached_end_of_feed = False
    all_feed_items = []

    # Fetch feed items until end of feed
    feedparser.USER_AGENT = USER_AGENT
    while not reached_end_of_feed:
        feed_url = 'https://www.google.com/finance/company_news?' \
                   + urllib.urlencode(args)
        feed = feedparser.parse(feed_url)
        all_feed_items += feed['items']
        reached_end_of_feed = len(feed['items']) != args['num']
        # Prepare for requesting next page
        args['start'] += args['num']

    return all_feed_items


def _word_normalization(text):
    """
    Normalize a string.
    
    Normalize a string by...
    - tokenizing it.
    - converting all letters to lowercase.
    - stemming words.
    - removing stopwords.
    
    """

    # Tokenize
    word_list = _tokenization(text)

    # Convert letters to lowercase
    word_list = [word.lower() for word in word_list]

    # Perform word stemming (using the Porter stemming algorithm)
    stemmer = nltk.PorterStemmer()
    word_list = [stemmer.stem(word) for word in word_list]

    # Remove stopwords    
    stopwords = nltk.corpus.stopwords.words('english')
    word_list = [word for word in word_list if word not in stopwords]
    
    return word_list
    
    
def _tokenization(text):
    """Perform a tokenization as in (Bird et al., 2009, page 111)"""
    pattern = r"""(?ux)                 # Set Unicode and verbose flag
              (?:[^\W\d_]\.)+                     # Abbreviation
              | [^\W\d_]+(?:-[^\W\d_])*(?:'s)?    # Words with optional hyphens
              | \d{4}                             # Year
              | \d{1,3}(?:,\d{3})*                # Number
              | \$\d+(?:\.\d{2})?                 # Dollars
              | \d{1,3}(?:\.\d+)?\s%              # Percentage
              | \.\.\.                            # Ellipsis
              | [.,;"'?!():-_`/]                  #
              """
    return nltk.regexp_tokenize(text, pattern)