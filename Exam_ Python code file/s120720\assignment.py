# DB module with basic crud.
# Later used in the project (twitter), and the plan
# is to store tweets to the DB and possibly fetch data and
# store some key data into a file on disk.
# The structures in this assignment are kept as simple as possible

import pymongo;
from pymongo import MongoClient;

class Database:
    def __init__(self,host,port):
        # these are to be used in final project
        OUT_REPORT = "report.txt"
        OUT_ENC = "utf-8"
        OUT_SETTING = "settings.bin"
        #self.client = MongoClient(host,port)
        self.client = MongoClient()
    	self.HANDLE = open("report.txt","r+")
        
    # TODO: save db_name to settings
    def connect(self,db_name):
        self.db = self.client[db_name]

    # TODO: save table_name to settings
    def table(self,table_name):
        self.table = self.db[table_name]

    # no need to sanitize, due to Mongo's structure
    def write(self,key,value):
        self.table.insert({key:value})

    # remove all matching key-value pairs
    def delete(self,key,value):
        self.table.remove({key:value})

    def update(self,bid,key,value):
        self.table.update( {'_id':pymongo.objectid(bid)},{key:value})

    # get latest 50 entries, sorted by id, maybe use date
    def read_latest_50(self):
        x = self.table.find().sort({_id:-1}).limit(50)
        return x
        
    # all entries? 
    def read_all(self,key,value):
        x = self.table.find({key:value})
        return x
        
    #settings? default settings? need to use encoding&error handling
    #generating some numbers to report, avg/var etc?
    def writeToFile(self,arg):
		self.HANDLE.write(arg)
        print "wrote to file"
        
	def read(self):
		self.HANDLE.seek(0)
		return self.HANDLE.read()
        
	def close(self):
		self.HANDLE.close()
		print "file closed"
        
# test        
def main():
	inst = Database()
	inst.connect("admin")
	inst.table("users")
	inst.insert('username','theuser')
if __name__ == '__main__':
	main()