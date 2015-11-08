"""
This is a program to download items from different RSS feeds and save them to sqlite database.

Example:
1. Create database (unless it already exists)
2. Add medium (eg. BBC)
3. Add feed (eg. http://feeds.bbci.co.uk/news/rss.xml)
4. Download items from chosen feed.
"""

__author__ = "Paulina Bien"

def create_database(c):
	c.execute('''CREATE TABLE media 
            (id integer primary key, name text)''')
	c.execute('''CREATE TABLE feeds 
				(id integer primary key, link text, title text, media_id integer, FOREIGN KEY(media_id) REFERENCES media(id))''')
	c.execute('''CREATE TABLE items 
				(id integer primary key, description text, link text, feed_id integer, FOREIGN KEY(feed_id) REFERENCES feeds(id))''')
			
def add_media(c):
	name = raw_input("Name: ")
	c.execute("INSERT INTO media(name) VALUES (?)", (name, ))

def add_feed(c):
	import sqlite3
	try:
		import feedparser
		media_id = raw_input("Media id: ")
		link = raw_input("Link: ")
		d = feedparser.parse(link)
		title = d.feed.title
		c.execute("INSERT INTO feeds(link, title, media_id) VALUES (?, ?, ?)", (link, title, media_id))
	except sqlite3.IntegrityError:
		print "Foreign key constraint failed"
	except AttributeError:
		print "Wrong RSS link"
	
def print_media(c):
	print'%2s\t%3s' % ("Id", "Name")
	for row in c.execute('SELECT * FROM media'):
		print'%2s\t%3s' % (row[0], row[1])
	
def print_feeds(c):
	print'%2s\t%3s' % ("Id", "Title")
	for row in c.execute('SELECT * FROM feeds'):
		print'%2s\t%3s' % (row[0], row[2])
		
def count_items(c):
	feed_id = raw_input("Feed_id: ")
	for row in c.execute('SELECT count(*) FROM items WHERE feed_id=?', feed_id):
		print row[0]
		
def add_items(c):
	import feedparser
	feed_id = raw_input("Feed id: ")
	row = c.execute('SELECT link FROM feeds WHERE id=?', feed_id)
	r = row.fetchone()
	if r == None:
		print "No feed"
	else:
		link = r[0]
		d = feedparser.parse(link)
		for entry in d.entries:
			if 'description' in d.feed:
				description = entry.description
			else:
				descritpion = entry.summary
			link = entry.link
			c.execute("INSERT INTO items(description, link, feed_id) VALUES (?, ?, ?)", (description, link, feed_id))
		
def delete_media(c):
	import sqlite3
	try:
		id = raw_input("Media id: ")
		c.execute('DELETE FROM media WHERE id=?', id)
	except sqlite3.IntegrityError:
		print "Foreign key constraint failed"

def delete_feed(c):
	import sqlite3
	try:
		id = raw_input("Feed id: ")
		c.execute('DELETE FROM feeds WHERE id=?', id)
	except sqlite3.IntegrityError:
		print "Foreign key constraint failed"
		
def delete_items(c):
	import sqlite3
	try:
		id = raw_input("Feed id: ")
		c.execute('DELETE FROM items WHERE feed_id=?', id)
	except sqlite3.IntegrityError:
		print "Foreign key constraint failed"

def main():
	import sqlite3, sys
	conn = sqlite3.connect('RSS.db')
	db = conn.cursor()
	db.execute('PRAGMA foreign_keys = ON')
	functions = dict(a=print_media, b=print_feeds, c=count_items, d=add_media, e=add_feed, f=add_items, g=create_database, h=delete_media, i=delete_feed, j=delete_items, q=exit)
	while True:
		print "\na - list media\nb - list feeds\nc - count items from feed\nd - add media\ne - add feed\nf - download items\ng - create tables\nh - delete media\ni - delete feed\nj - delete items from feed\nq - quit"
		action = raw_input("Choose action: ")
		if action != 'q':
			try:
				functions[action](conn)
				conn.commit()
			except KeyError:
				print "Wrong letter!"
		else:
			conn.commit()
			conn.close()
			sys.exit(0)E:
	
if __name__ == "__main__":
    main()