'''
Kaelan Lupton
20036736
I confirm that this submission is my own work and is consistent with the
Queen's regulations on Academic Integrity. 

1. I hypothesize that double hashing will produce the required performance
standards with a smaller table size than quadratic probing. The latter,
while good at avoiding primary clustering, is occasionally prone to
secondary clustering. Due to this, I expect double hashing, with correctly
chosen tables sizes and hashing functions, will produce better results.

2. To translate a string to an integer value, I will sum the ASCII values
of each character in the string, then do modular division by m, the number
of spaces in the table, to ensure the number always falls in the table’s
range.

3. I based my experiments off the models used on code2begin.blogspot.com, linked here:

http://code2begin.blogspot.com/2017/01/hashing-with-quadratic-probing.html

This was the framework I used, editing it to fit my needs and to ensure I understood
what each piece of code was doing itself. I also implemented my own hash function. 

4. I based my experiments off the models used on code2begin.blogspot.com, linked here:

http://code2begin.blogspot.com/2017/02/double-hashing.html

This was the framework I used, editing it to fit my needs and to ensure I understood
what each piece of code was doing itself. I also implemented my own hash function. 

'''


import numpy as np
import matplotlib.pyplot as plt

class doubleHashTable:
    '''
    Hash Table class for using double hashing.
    This class utilizes two hash functions to place
    items from a list into a hash table.
    '''
    
    def __init__(self, x):
        '''
        Initializes the class.
        
        self - the class itself.
        x - integer to indicate the size of the table.
        '''
        self.size = x
        self.table = list(0 for i in range(self.size))
        self.count = 0
        self.comparisons = 0
      
    
    def isFull(self):
        '''
        Checks if a table is already full.
        
        self - the class itself.
        '''
        if self.count == self.size:
            return True
        else:
            return False
   

    def h1(self, element, x):
        '''
        First hash function used to determine position on hash table.
        This function sums the squared ASCII value modularly divided
        by x of each character in the given string.
        
        self - the class itself.
        element - the string to be hashed.
        x - integer to modularly divide by to change hash function.
        '''        
        total = 0
        for i in range(len(element)):
            total = total + ((ord(element[i])**2)*x)
        return total%self.size
       
        
    def h2(self, element, x):
        '''
        Second hash function used to determine position on hash table.
        This function sums the ASCII values of each character and squares
        the total, then modularly divides that number by x.
        
        self - the class itself.
        element - the string to be hashed.
        x - integer to modularly divide by to change hash function.
        '''
        total = 0
        for i in range(len(element)):
            total = total + ord(element[i])
        return total**2 % x
           
    def doubleHashing(self, element, position, a, b):
        '''
        This method words to resolve collisions with double hashing.
        
        self - the class itself.
        element - the string to be filed in the hash table.
        position - the current position.
        a - the constant subbed into the first hash function.
        b - the constant subbed into the second hash function.
        '''
        posFound = False
        exceed = False
        i = 1

        while i <= self.size:
            newPosition = (self.h1(element, a) + (i*self.h2(element, b))) % self.size
            if self.table[newPosition] == 0:
                posFound = True
                break
            else:
                i += 1
                if i >= 5:
                    exceed = True
        return posFound, newPosition, exceed
 
       
    def insert(self, element, a, b):
        '''
        Insert an element into a hash table.
        
        self - the class itself.
        element - the string to be inserted.
        a - the constant subbed into the first hash function.
        b - the constant subbed into the second hash function. 
        '''
        
        if self.isFull():
            print("Hash Table Full")
            return False
           
        didExceed = False
        
        isStored = False
       
        position = self.h1(element, a)
           
        if self.table[position] == 0:
            self.table[position] = element
            isStored = True
            self.count += 1
       
        else:
            isStored, position, exceed = self.doubleHashing(element, position, a, b)
            if isStored:
                self.table[position] = element
                self.count += 1
                if exceed:
                    didExceed = True
 
        return isStored, didExceed
    
        
def main():
    '''
    Main function of the program.
    '''
    
    # lists for holding data to iterate through
    h1Options = [7,2,11]
    h2Options = [5,2,13]
    tableSizes = [4001,4003,4007,4013,4019,4073,4591,5101,6907,7817,8713,9973]
    
    # will hold success rates of each hash function pair
    h1List = []
    h2List = []
    h3List = []
    
    hList = [h1List, h2List, h3List]
    
    # iterate throughe each hash function pair
    for j in range (0,3):
        
        bestSize = 100000000

        # iterate through each table size
        for k in range (len(tableSizes)):
            numberExceeded = 0
            table = doubleHashTable(tableSizes[k])

            # read file, assign to list
            with open('235.txt') as f:
                content = f.readlines()
                content = [x.strip() for x in content]

            randomSample = []

            # take random sample of 4000 strings from file list
            for i in range (0,4000):
                choice = np.random.choice(content)
                randomSample.append(choice)
                content.remove(choice)

            for i in range (0, len(randomSample)):
                test, num = table.insert(randomSample[i], h1Options[j], h2Options[j])
                if num:
                    numberExceeded += 1
            if numberExceeded < 800:
                if tableSizes[k] < bestSize:
                    bestSize = tableSizes[k]
                    
            print("Table Size: "+str(tableSizes[k])+". Limit exceeded " + str(numberExceeded)+" times, "+str((numberExceeded/4000)*100)+"%")
            hList[j].append(100-((numberExceeded/4000)*100))
            
        print("Smallest acceptable table size is " + str(bestSize)+"\n")

    # plotting the found data
    h1Plot = plt.scatter(tableSizes,h1List, alpha=0.3)
    h2Plot = plt.scatter(tableSizes,h2List, alpha=0.3)
    h3Plot = plt.scatter(tableSizes,h3List, alpha=0.3)
    plt.xscale('log')
    plt.title('Plotting the effects of various hash functions on double hashing')
    plt.xlabel('Table size')
    plt.ylabel('Success rate')
    plt.legend((h1Plot, h2Plot, h3Plot),
           ('h1 = 7, h2 = 5', 'h1 = 2, h2 = 2', 'h1 = 11, h2 = 13'),
           fontsize=8)
    plt.show()        
        
main()





