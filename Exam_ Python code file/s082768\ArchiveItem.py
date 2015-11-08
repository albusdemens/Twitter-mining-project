# -*- coding: utf-8 -*-
"""
This class is inspired by the trouble my scout group has in keeping track on
which items are stored where in our scout hut.

This class represents the backend of a system that keeps track of items in
a storage facility here called an archive.

It is built around the idea that moving an item around should be easy, and 
that an item can itself contain other items. Moving an item (switching parent)
will automatically move whatever items that is contained in the moved item.

Another feature is the default option of inherited hits. This means that any 
search term hits, that an ancestor has wil be shared with the item. thus it
is possible not only to search for an item, but also a room or closet which will
then return any contents of these.


"""      
class ArchiveItem():
    """
    item in Archive
    An item has a parent corresponding to the location where it can be found
    and optionally children that can be found inside the item
    along with name keyWords can be added that will count towards search term 
    hits.
    
    There are 3 types of operations on this class:
        "family management" i.e. manipulation of the network/graph
        keyWord management
        search functions
    """
    def __init__(self,parent,name,keyWordStr):
        self.parent=parent
        self.children = []
        self.name=name
        self.keys = keyWordStr.split()
        
    def _print(self):
        print("name: "+self.name)
            
        if(self.parent!=None):
            print("key words:")
            for key in self.keys:
                print("- "+key)
                
            print("location:")
            indent = ""
            for parent in self.ancestors():
                if(parent!=self):
                    print(indent+"- "+parent.name)
                    indent+="   "
        else:
            print("__root item__")
            
        print("children:")
        for child in self.children:
            print("- "+child.name)
            
    def addKeyWord(self,keyWord):
        if(keyWord not in self.keys):
            self.keys+= [keyWord]
            
    def removeKeyWord(self,keyWord):
        if(keyWord in self.keys):
            self.keys.remove(keyWord)
     
# ancestors() returns ancestors as list of class object      
    def ancestors(self): 
        if(self.parent==None):
            return [self]
        return  self.parent.ancestors() + [self]

# Family management functions 
    def addChild(self,newChild):
        if newChild not in self.children:
            self.children += [newChild]
    
    def removeChild(self,child):
        if child in self.children:
            self.children.remove(child)

    def switchParent(self,newParent):
        if(self.parent!=newParent):
            if self.parent!=None:
                self.parent.removeChild(self)            
            self.parent=newParent
            self.parent.addChild(self)
    def adoptChild(self,newChild):
        newChild.switchParent(self)
        
    def adoptAll(self,oldParent):
        for child in oldParent.children:
            self.adoptChild(child)
    
    def orphan(self):
        if self.parent!=None:
            self.parent.removeChild(self)
        self.parent=None
# contract() removes itself as a node and donates alle children to its parent
    def contract(self):
        if self.parent==None:
            for child in self.children:
                child.orphan()
        else:
            self.parent.adoptAll(self)
            self.orphan()
        
    def cleanUp(self):
        for key in self.keys:  #remove keys in key register
            self.removeKeyWord(key)
            self.parent.removeChild(self)
        for child in self.children: # contract node in archive
            child.switchParent(self.parent)
            self.parent.addChild(child)
    

# Search functions 
# getHits(searchTerms counts hw many search terms match name or keys. case is ignored
    def getHits(self,searchTerms):
        if(self.name.lower() in map(lambda x:x.lower(),searchTerms)):
            hits = 1
        else:
            hits = 0
        for keyWord in self.keys:
            if(keyWord.lower() in map(lambda x:x.lower(),searchTerms)):
                hits+=1
        return {self:hits}
        
    def recurSearch(self,ancestorHits,searchTerms,inheritHits=True):
        result = self.getHits(searchTerms)
        if inheritHits:
            result[self]+=ancestorHits
        for child in self.children:
                result.update(child.recurSearch(result[self],searchTerms,inheritHits=inheritHits))
        return result
        
    def search(self,searchTerms):
        results = self.recurSearch(0,searchTerms)
        sortedRes = dict()
        for res in results.iteritems():
            if(sortedRes.has_key(res[1])):
                sortedRes[res[1]] += [res[0]]
            else:
                sortedRes[res[1]] = [res[0]]
        return sortedRes

    def searchAndPrint(self,searchTerms,hitThres):
        sortedRes = self.search(searchTerms) # return node:hits pairs
        
        for hits in sorted(sortedRes.keys(),reverse=True):
            if hits>hitThres:
                print("hits="+str(hits))
                for item in sortedRes[hits]:
                    item._print()
                    print(" ")
                    

items = {"trop":ArchiveItem(None,"Tropslokale","lokale rum trop")}
items.update({"skab1":ArchiveItem(None,"Skab1","skab grenmateriel")})
items["skab1"].switchParent(items["trop"])
items["trop"].searchAndPrint(["rum","skab"],0)