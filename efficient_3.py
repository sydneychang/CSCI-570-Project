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

def bottomUpPass(string1Len: int, string2Len: int, inputString1: str, inputString2: str) -> list: 
    memoizedArray = [[0 for x in range(string1Len + 1)] for y in range(string2Len + 1)] 

    for i in range(string1Len + 1):
        memoizedArray[0][i] = i * delta

    for i in range(string2Len + 1):
        memoizedArray[i][0] = i * delta
    
    for j in range(1, string2Len + 1):                                               
        for i in range(1, string1Len + 1):
            memoizedArray[j][i] = min(
                memoizedArray[j-1][i-1] + mismatchCosts[inputString2[j-1]][inputString1[i-1]],
                memoizedArray[j-1][i] + delta,
                memoizedArray[j][i-1] + delta
            )
    return memoizedArray

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
    memoizedArray1 = bottomUpPass(string1LenHalved, string2Len, inputString1, inputString2)                                                      #first half of X
    memoizedArray2 = bottomUpPass(string1LenRemainder, string2Len, inputString1Reversed, inputString2Reversed)   #last half of X
    
    #add and find min for optimal splitting point (min cost of alignment for split). final col of each array contains opt costs of alignment.
    costOfAlignmentArr = []
    for i in range (string2Len +1): 
        costOfAlignmentArr.append(memoizedArray1[i][string1LenHalved] + memoizedArray2[string2Len-i][string1LenRemainder]) #(k chars of Y) + (n-k chars of Y)
    costOfOptimalAlignment = min(costOfAlignmentArr)
    optAlignmentY1 = costOfAlignmentArr.index(costOfOptimalAlignment)
    optAlignmentY2 = string2Len - optAlignmentY1

    #topdown for first half
    alignedFirstHalf = topDownPass(string1LenHalved, optAlignmentY1, inputString1, inputString2, memoizedArray1)
    firstHalfX = "".join(reversed(alignedFirstHalf[0]))
    firstHalfY = "".join(reversed(alignedFirstHalf[1]))

    #topdown for last half
    alignedLastHalf = topDownPass(string1LenRemainder, optAlignmentY2, inputString1Reversed, inputString2Reversed, memoizedArray2)
    lastHalfX = "".join((alignedLastHalf[0]))       #don't have to reverse bc the array had reversed X and Y already
    lastHalfY = "".join((alignedLastHalf[1]))

    #conquer - concatenating the string
    fullyAlignedX = firstHalfX + lastHalfX
    fullyAlignedY = firstHalfY + lastHalfY
    
    #write to file
    f = open(os.path.join(cwd, sys.argv[2]), "w")                                                #ex: 2nd CLA could be basicAlgOutput.txt
    f.write("%d\n" % costOfOptimalAlignment)
    f.write(fullyAlignedX + "\n" + fullyAlignedY + "\n")
    f.write("%f\n" % time_wrapper())
    f.write("%f\n" % process_memory())
    f.close()

    