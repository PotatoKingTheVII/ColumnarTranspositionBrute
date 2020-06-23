import math
from itertools import permutations
import csv
import re
import numpy as np
from multiprocessing import Pool

###USER OPTIONS###
threads = 8 #Advised to set it to your actual thread count or less
permutation_length = 8  #Takes around 2 minutes for 9 on an 8 thread
ciphert = "lditel sel!s Wh moitp TaaHrselo  s"





def word2key(word):     #Words to numbered key starting at 0
        keyList = []
        permutation_key = []
        for i in range(0,len(word)):
            keyList.append([word[i],(i+0)])
        keyList = sorted(keyList)
        
        for i in range(0,len(keyList)):
            permutation_key.append(keyList[i][1])

        return permutation_key

def decrypttrans(ciphertext, key):
    ##First we need to get the position of any empty cells for this key
    ##To do this we simulate encrypting a message of length of the ciphertext with the given key and inspect the result
    permutation_key = key

    ciphertextMask = "*"*len(ciphertext)    #Content doesn't matter, only length for this part
    grid = []   #The full grid with ciphertext
    currentRow = [] #The letters for the current row of the grid
    colNumbers = len(permutation_key)   #Max number of columns
    rowNumbers = math.ceil( len(ciphertextMask)/colNumbers)  #Max number of rows
    currentLetter = 0   #Keep track of which letter index we're on
    
    for i in range(0, rowNumbers):  #For each row
        for j in range(0,colNumbers):   #For each column
            try:    #Either add the current plaintext letter
                currentRow.append(ciphertextMask[currentLetter]) 
            except: #Or there's no plaintext left and add an empty indicator
                currentRow.append("")
            currentLetter += 1  #Next letter
        grid.append(currentRow) #Add current full row to the grid
        currentRow = []


    #Get the columms of this grid in an array
    columns = []
    currentColumn = []
    for i in range(0,colNumbers):
        for j in range(0,rowNumbers):
            currentColumn.append(grid[j][i])
        columns.append(currentColumn)
        currentColumn = []


    #Rearrange these columns according to the key
    rearrangedColumns = []
    for i in range(0,colNumbers):
        rearrangedColumns.append(columns[permutation_key[i]])
 
    ##At this point these columns will reflect any empty points for the ciphertext and given key
    ##We then create a grid and fill it out with the ciphertext following these empty points vertically then across
    columns = []
    currentColumn = []
    currentLetter = 0
    for i in range(0,colNumbers):
        for j in range(0,rowNumbers):
            if(rearrangedColumns[i][j]!=""):
                currentColumn.append(ciphertext[currentLetter])
                currentLetter+=1
            else:
                currentColumn.append("")
            
        columns.append(currentColumn)
        currentColumn = []


    #At this point we now have the correctly filled out grid with empty points
    #Now we re-arrange it in order of the key
    rearrangedColumns = [None]*colNumbers
    for i in range(0,colNumbers):
        rearrangedColumns[permutation_key[i]] = columns[i]


    #Now read this off for the final plaintext
    plaintext = ""
    for i in range(0,rowNumbers):
        for j in range(0,colNumbers):
            plaintext += rearrangedColumns[j][i]
    return plaintext


def actual_percentage(text):    #Return percentages of listed bigrams from file in text
    text = text.lower()
    occurances = []
    for bigram in data: #Cycle through all bigrams
        if(text.find(bigram[0])!=-1):   #Check if any actually exist in text
            occurances.append(len(re.findall(bigram[0],text)))  #If so check how many (intensive)
        else:
            occurances.append(0)    #Otherwise there aren't any so set to 0
    actual_percentages = np.divide(occurances,sum(occurances))
    return actual_percentages


def fitness(text):  #Calc with chi squared bigram comparison
    text = (text.replace(" ",""))
    freq = actual_percentage(text)
    #####CHI SQUARED#####
    expected = expected_percentages
    chi = 0
    for i in range(0,len(freq)):
        chitop = (freq[i]-expected[i])**2
        chibottom= expected[i]

        chi+=(chitop/chibottom)
    return chi


def fitnessList(textList):  #For use with multiprocess, does fitness on a list of texts
    fullList = []
    for i in range(0,len(textList)):    #Add chi values to each possibility
        fullList.append([textList[i][0],fitness(textList[i][0]),textList[i][1]])
 
    return fullList

def decrypttransList(keyList):  #For use with multiprocess, decrypts text with the given list of keys
    fullList = []
    for i in range(0,len(keyList)):    #Add chi values to each possibility
        fullList.append([decrypttrans(ciphert,keyList[i]),keyList[i]])  #Add the used key along with the decrypted result to keep track
 
    return fullList


#####Chi squared section with bigrams#####
expected_percentages = []
with open('bigramfreq.csv', newline='') as csvfile:    #Get expected freq from file
    data = list(csv.reader(csvfile))
    for bigram in data:
        expected_percentages.append(float(bigram[1]))
#File from http://practicalcryptography.com/media/cryptanalysis/files/english_bigrams_1.txt



if __name__ == '__main__':  #Only run this section if it's the main script running, not a sub-process from multiprocessing
    #Run through all combinations of transposition
    key_permutations = []
    for i in range(1,permutation_length+1):
        currentPerms = list(permutations([*range(0,i)]))
        key_permutations += currentPerms


    #We split the list of combinations up into chunks for the number of processes we're using
    comboChunks = np.array_split(key_permutations, threads)
    with Pool(threads) as p:
        results = (p.map(decrypttransList, comboChunks ))
        
    allcombos = [item for sublist in results for item in sublist] #Combine each thread's sublist


    #Write the unsorted combos to file
    with open("RawCombos.txt", "w") as fout:
        for combination in allcombos:
            fout.write(combination[0] +"        " + str([k+1 for k in combination[1][:]]) + "\n")
    print("Dumped raw combinations, calculting fitness...")
        

    #We split the list of combinations up into chunks for the number of processes we're using
    comboChunks = np.array_split(allcombos, threads)
    with Pool(threads) as p:
        results = (p.map(fitnessList, comboChunks))

        
    orderedlist = [item for sublist in results for item in sublist] #Combine each thread's sublist
    orderedlist = sorted(orderedlist, key=lambda chi: chi[1])   #Sort list for lowest chi score first

        
    #Output results to ordered file
    with open("OrderedList.csv", "w") as fout:
        for i in range(0,len(orderedlist)): #Write combo, rail, offset and fitness to file
            #When writing the key here we add one to each value so it's in the form expected starting at 1 not 0
            fout.write(orderedlist[i][0] +"     Key: "+ str([k+1 for k in orderedlist[i][2][:]]) + " Fitness: " + str(orderedlist[i][1]) + "\n")
    print("\n\nDumped ordered list to file, finished\n")

