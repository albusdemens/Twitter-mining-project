# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 11:34:46 2013

@author: Alina
"""
import lxml.html
import scraperwiki

class Recepie( object ):
    #Create a recepie object.
    def __init__( self,name_recepie,ingredients_recepie,votes_recepie, site_recepies):
        self.name_recepie = name_recepie
        self.ingredients_recepie= ingredients_recepie #is a list of IngredientCouple
        self.votes_recepie = votes_recepie
        self.site_recepies = site_recepies
    def displayRecepie(self):
      return self.name_recepie,[p.displayIngredientCouple() for p in self.ingredients_recepie],self.votes_recepie 
          
    
class IngredientCouple( object ):
    #Create a ingredient-amount object.
    def __init__( self, ingredient, amount):
        self.ingredient = ingredient
        self.amount = amount
    def displayIngredientCouple(self):
        return self.ingredient, self.amount


def parse(address):
    #Parser made for allrecepies.com
    #this parser is getting the name of each recepie and the ingredients 
    #and the review. 
    html = scraperwiki.scrape(address)
    root = lxml.html.fromstring(html)
    #ingredients    
    ingredientList = root.cssselect("ul.ingredient-wrap")
    mIngredientsList= []    
    for el in ingredientList:           
        group = el.cssselect("li label p")[0]
        name = group.cssselect("span#lblIngName")[0]
        amount = group.cssselect("span#lblIngAmount")[0]
        mIngredient = IngredientCouple(name.text,amount.text)
        mIngredientsList.append(mIngredient)
        
    #recepiename
    recepieName = root.cssselect("h1#itemTitle")[0]

    #reviews
    reviewWithText = root.cssselect("a#btnScrollToReview")[0]
    reviews =  reviewWithText.text[-4:-1]
    
    #create a recepie and return it
    recipes = Recepie(recepieName.text,mIngredientsList,reviews,"allrecipes.com")
    return recipes.displayRecepie()


print parse("http://allrecipes.com/Recipe/Baked-Chicken-Nuggets/Detail.aspx?evt19=1")    
  
        
