import os
import sys
from resource import * 
import time
import psutil

cwd = os.path.dirname(os.path.abspath(__file__))    #global variables
delta = 30                                          #gap penalty
mismatchCosts = {                                   #alpha values
    "A": {"A": 0, "C": 110, "G" : 48, "T" : 94},
    "C": {"A": 110, "C": 0, "G": 118, "T" : 48},
    "G": {"A": 48, "C": 118, "G": 0, "T": 110},
    "T": {"A": 94, "C": 48, "G": 110, "T": 0}
}

def process_memory() -> int:
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed

def time_wrapper(): 
    start_time = time.time() 
    #call algorithm
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken

def inputStringGenerator() -> list:           #reads from txt file and creates the 2 strings of input for sequence alignment
    count = 0
    inputString1 = ""
    inputString2 = ""        
    with open(os.path.join(cwd, "SampleTestCases", sys.argv[1]), "r", encoding="UTF-8") as file:     #ex: 1st CLA could be "input5.txt"
        while line := file.readline().rstrip():
            if(line.isalpha() and not inputString1): 
                inputString1 = line
                count += 1
                continue
            elif(line.isalpha() and not inputString2):
                inputString2 = line
                count += 1
                continue

            line = int(line) + 1
            if(count == 1):
                inputString1 = inputString1[:line] + inputString1 + inputString1[line:]
            else:
                inputString2 = inputString2[:line] + inputString2 + inputString2[line:]

    return [inputString1, inputString2]

def getCostOfOptimalAlignments(string1Len: int, string2Len: int, inputString1: str, inputString2: str, memoizedArray: list) -> list:  #using only 2 columns, return the final col array
    for i in range(1, string1Len + 1):
        memoizedArray[1][0] = i * delta                        #initialize the first value of the 2nd row
        for j in range(1, string2Len + 1):                                               
            memoizedArray[1][j] = min(
                memoizedArray[0][j-1] + mismatchCosts[inputString2[j-1]][inputString1[i-1]],
                memoizedArray[0][j] + delta,
                memoizedArray[1][j-1] + delta
            )
        temp = memoizedArray[0]                     #swap array rows to build the next set of optimal values.
        memoizedArray[0] = memoizedArray[1]
        memoizedArray[1] = temp                     #next iteration's "bottom up pass" will overwrite the previous row
    return memoizedArray[0]                         #the final swap puts the correct alignment costs in the 0th position

if __name__ == "__main__":             #main driver
    inputs = inputStringGenerator()
    inputString1 = inputs[0]
    inputString2 = inputs[1]

    string1Len = len(inputString1)
    string2Len = len(inputString2)
    inputString1Reversed = "".join(reversed(inputString1))
    inputString2Reversed = "".join(reversed(inputString2))
    #print(inputs[0] + "\n" + inputs[1])

    #divide - half of X and all of Y
    string1LenHalved = string1Len//2
    string1LenRemainder = string1Len - string1LenHalved
    memoizedArray1 = [[0 for y in range(string2Len + 1)] for x in range(2)] 
    memoizedArray2 = [[0 for y in range(string2Len + 1)] for x in range(2)] 
    for i in range(string2Len + 1):
        memoizedArray1[0][i] = i * delta
        memoizedArray2[0][i] = i * delta        
    
    optimalCostsArray1 = getCostOfOptimalAlignments(string1LenHalved, string2Len, inputString1, inputString2, memoizedArray1)              
    optimalCostsArray2 = getCostOfOptimalAlignments(string1LenRemainder, string2Len, inputString1Reversed, inputString2Reversed, memoizedArray2)  
    
    costOfFullStringAlignmentArr = []
    for i in range (string2Len + 1):                                  #add and find min for optimal splitting point (min cost of alignment for split).
        costOfFullStringAlignmentArr.append(optimalCostsArray1[i] + optimalCostsArray2[string2Len-i]) #(k chars of Y) + (n-k chars of Y)
    costOfOptimalAlignment = min(costOfFullStringAlignmentArr)
    optAlignmentY1 = costOfFullStringAlignmentArr.index(costOfOptimalAlignment)
    optAlignmentY2 = string2Len - optAlignmentY1
    print(costOfOptimalAlignment)

    #topdown for first half
    '''alignedFirstHalf = topDownPass(string1LenHalved, optAlignmentY1, inputString1, inputString2, memoizedArray1)
    firstHalfX = "".join(reversed(alignedFirstHalf[0]))
    firstHalfY = "".join(reversed(alignedFirstHalf[1]))

    #topdown for last half
    alignedLastHalf = topDownPass(string1LenRemainder, optAlignmentY2, inputString1Reversed, inputString2Reversed, memoizedArray2)
    lastHalfX = "".join((alignedLastHalf[0]))       #don't have to reverse bc the array had reversed X and Y already
    lastHalfY = "".join((alignedLastHalf[1]))

    #conquer - concatenating the string
    fullyAlignedX = firstHalfX + lastHalfX
    fullyAlignedY = firstHalfY + lastHalfY'''
    
    #write to file
    '''f = open(os.path.join(cwd, sys.argv[2]), "w")                                                #ex: 2nd CLA could be basicAlgOutput.txt
    f.write("%d\n" % costOfOptimalAlignment)
    f.write(fullyAlignedX + "\n" + fullyAlignedY + "\n")
    f.write("%f\n" % time_wrapper())
    f.write("%f\n" % process_memory())
    f.close()'''





#potential scrap
def topDownPass(string1Len: int, optAlignmentInY: int, inputString1: str, inputString2: str, memoizedArray: list) -> list:
    m, n = string1Len, optAlignmentInY
    alignedString1, alignedString2 = "", ""
    while(m > 0 or n > 0): 
        if memoizedArray[n][m] == memoizedArray[n-1][m-1] + mismatchCosts[inputString1[m-1]][inputString2[n-1]]:
            alignedString1 += inputString1[m-1] 
            alignedString2 += inputString2[n-1]
            m -= 1   
            n -= 1
        elif memoizedArray[n][m] == memoizedArray[n-1][m] + delta:   #elif memoizedArray[n][m] == memoizedArray[n][m-1] + delta:
            alignedString1 += "_"                                    #alignedString1 += inputString1[m-1]
            alignedString2 += inputString2[n-1]                      #alignedString2 += "_"
            n -= 1                                                   #m -= 1
        else:
            alignedString1 += inputString1[m-1]                      #alignedString1 += "_"
            alignedString2 += "_"                                    #alignedString2 += inputString2[n-1]
            m -= 1       
    return [alignedString1, alignedString2]                                            #n -= 1