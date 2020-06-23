import math

def word2key(word): #Convert the given word to a numerical key starting at 0
    keyList = []
    permutation_key = []
    for i in range(0,len(word)):
        keyList.append([word[i],(i+0)])
    keyList = sorted(keyList)
    
    for i in range(0,len(keyList)):
        permutation_key.append(keyList[i][1])

    return permutation_key

def encrypttrans(plaintext, key):
    #First calculate the numerical values from the key
    permutation_key = word2key(key)


    #Make array consisitng of arrays for each row in grid of plaintext
    grid = []   #The full grid with plaintext
    currentRow = [] #The letters for the current row of the grid
    colNumbers = len(permutation_key)   #Max number of columns
    rowNumbers = math.ceil( len(plaintext)/colNumbers)  #Max number of rows
    currentLetter = 0   #Keep track of which letter index we're on
    
    for i in range(0, rowNumbers):  #For each row
        for j in range(0,colNumbers):   #For each column
            try:    #Either add the current plaintext letter
                currentRow.append(plaintext[currentLetter]) 
            except: #Or there's no plaintext left and add an empty
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

    
    #Read this rearranged grid off for the ciphertext
    ciphertext = ""
    for i in range(0,colNumbers):
        for j in range(0,rowNumbers):
            ciphertext += rearrangedColumns[i][j]
    return ciphertext




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
            except: #Or there's no plaintext left and add an empty
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


    
print(encrypttrans("Hello world! This is a test", "test"))
print(decrypttrans("e lT aslwdhi tHor s elo!ist", word2key("test")))

