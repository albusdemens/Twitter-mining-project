import random

# Defining function that takes in a list and sorts it
# input: list
# output: same list, just sorted. 
def SortList(l):
    
    for i in range(1,len(l)):
        #Takes the next value in the list
        current = l[i]
        index = i
        
        # As long as the current value is smaller we move it down the list
        while index > 0 and l[index-1] > current:
            l[index] = l[index-1]
            index = index-1
        
        l[index] = current

# Defining function that finds a specific value v or the value closest to v in a list 
# input: integer and list
# output: index
def FindClosestValue(v,l):
    
    # We start looking at the entire list
    start = 0
    stop = len(l)-1
    
    while start < stop:
        #Looks at the value in the middel of current list
        middel = (start+stop)//2
        
        # For each iteration we keep restricting the range 
        if l[middel] < v:
            start = middel + 1   
        elif l[middel] > v:
            stop = middel - 1   
        else:
            return middel
    
    # If we get here, it means that the v isn't in the list
    # Precautions when the value we are seeking is the first or last in the list
    if v < l[0] or v > l[len(l)-1]: return start
    
    v1 = abs(v-l[start])
    v2 = abs(v-l[start-1])
    v3 = abs(v-l[start+1])
    if min(v1,v2,v3) == v1: return start
    elif min(v1,v2,v3) == v2: return start-1
    else: return start+1

# Defing a list a with length 1000, consisting of random numbers from 1 to 10000
a = []
for i in range(1000):
    r = random.randint(1,10000)
    a.append(r) 

SortList(a)

Value = ''
# End program when exit is entered
while(Value != 'exit'):
	Value = raw_input('Enter integer or exit : ')
	# If it is a value
	if Value.isdigit():
		VaIn = FindClosestValue(int(Value), a)
		print 'The closest value is ' +str(a[VaIn])+ ' at index ' + str(VaIn)