#To run the code, write

#from ishashad import ishashad
#then ishashad(number)

def ishashad(n):
    if n % sum(map(int,str(n))) == 0:
        print("True")
    else:
    	print("False")
    	return