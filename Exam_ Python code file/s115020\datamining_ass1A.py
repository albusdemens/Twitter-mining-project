# -*- coding: utf-8 -*-

# name: Morten Frandsen
# std-nr: s115020
# course: 02819 Data Mining using Python

# This class is a simple and primitive version of a matrix.
# I've tried to make this for the sake of practicing my python.
# So fare it supports addition, multiplication and it can be inverted.
class aSimpleMatrix(object):
    
    
    # Here the class is initialized
    # It takes either 0,1,2 or 3 arguments.
    def __init__(self,*args):
        
        # Zero arguments given
        if (len(args) == 0):
            self.m = 0
            self.n = 0		# dimensions will be 0x0
            self.matrix = []	# and no values , empty list
            
        # One argument given
        elif (len(args) == 1):
            self.m = len(args)		# 
            self.n = len(args[0])	# save dimensions, m x n
            for i in args:
                if (len(i) != self.n): # all rows in the matrix must be of same size
                    raise ValueError("Matrix size doesn't match input")

            # save the input to the class object
            templiste = [0] * self.n
            self.matrix = []
            for i in range(self.m):
                self.matrix.append(list(templiste))
    
            for i in range(self.m):
                for j in range(self.n):
                    self.matrix[i][j] = args[i][j]
        
        # Two arguments given
        elif (len(args) == 2):       
            self.m,self.n = args
            
	    # creates a m x n matrix initialized with 0's
            templiste = [0] * self.n
            self.matrix = []
            for i in range(self.m):
                self.matrix.append(list(templiste))
            
        # Three arguments given
        elif (len(args) == 3):       
            self.m,self.n,inputValues = args
            if (self.m != len(inputValues)):
                raise ValueError("Matrix size doesn't match input")
            for i in inputValues:
                if (len(i) != self.n):
                    raise ValueError("Matrix size doesn't match input")
                    
	     # save the input to the class object
            templiste = [0] * self.n
            self.matrix = []
            for i in range(self.m):
                self.matrix.append(list(templiste))
    
            for i in range(self.m):
                for j in range(self.n):
                    self.matrix[i][j] = inputValues[i][j]
        
        # Any other amount of arguments given
        else:                        
            raise ValueError("Inapropriot amount of arguments")
            
        return
        
    # this will overwride the basic '+'-operater
    # the following code will run instead
    def __add__(self,other):
        if (type(other) != aSimpleMatrix):	# both must of course be of type aSimpleMatrix
            raise TypeError("Both operands need to be of the same type")
        if ((self.m != other.m) or (self.n != other.n)):
            raise ValueError("The dimension of the matrices must match")	# they must match in dimensions
        else:
            temp = aSimpleMatrix(self.m,self.n)	# creates a new object were result is saved
            for i in range(self.m):
                for j in range(self.n):
                    temp.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]	# add together each element
        return temp								# and return the result

    # this will overwride the basic '*'-operater
    # the following code will run instead
    def __mul__(self,other):
        if (type(other) != aSimpleMatrix):
            raise TypeError("Both operands need to be of the same type")	# both must of course be of type aSimpleMatrix
        if (self.m != other.n):
            raise ValueError("The dimension of the matrices must match")	# they must match in dimensions
        
        temp = aSimpleMatrix(self.m,other.n) 	# creates a new object were result is saved
        for a in range(self.m):			# the dimensions is given by the to other matrices
            for b in range(other.n):
                for c in range(other.m):
                    temp.matrix[a][b] += self.matrix[a][c]* other.matrix[c][b]
        return temp

    # this will overwride the basic 'print'-operater , or 'str()'-operater
    # the following code will run instead
    def __str__(self):
        if (len(self.matrix) == 0):	# in case the matrix is empty
            return "[]"
        else:				# in other case:
            text = "[ "			# add the numbers to a string, seperate each number with |
            for a in range(len(self.matrix)):
                for b in range(len(self.matrix[0])):
                    text = text + str(self.matrix[a][b]) + " | "
                text = text[:-2] + "\n  "	# i've tried to make it look good
            text = text[:-4] + " ]"		# but at the moment it only really works for small numbers.
        return text        		# return the text that have been collected
        

    # This is the classic transpose matrix as a function call
    def transpose(self):
        newMatrix = aSimpleMatrix(self.n,self.m)
        m_new = self.n
        n_new = self.m
        
        print newMatrix        
        
        for i in range(m_new):
            for j in range(n_new):
                newMatrix[i][j] = self.matrix[j][i]
        
        self.m = m_new
        self.n = n_new
        self.matrix = newMatrix
        return
        
    # I wanted to make use of cherryPy aswell, and have the matrix display in a browser
    # but I didn't make that work in time
    #def showMatrixInBrowser():
        #index.exposed = True
        #cherrypy.quickstart(aSimpleMatrix.showMatrixInBrowser())
