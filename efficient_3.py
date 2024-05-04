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

if __name__ == "__main__":             #main driver
    inputs = inputStringGenerator()
    inputString1 = inputs[0]
    inputString2 = inputs[1]

    string1Len = len(inputString1)
    string2Len = len(inputString2)

    print(inputs[0] + "\n" + inputs[1])

    #divide - half of X and all of Y
    #first half of X
    string1LenDivided = string1Len//2   #floor
    memoizedArray1 = [[0 for x in range(string1LenDivided + 1)] for y in range(string2Len + 1)] 

    for i in range(string1LenDivided + 1):
        memoizedArray1[0][i] = i * delta

    for i in range(string2Len + 1):
        memoizedArray1[i][0] = i * delta
    
    for j in range(1, string2Len + 1):                                               
        for i in range(1, string1LenDivided + 1):
            memoizedArray1[j][i] = min(
                memoizedArray1[j-1][i-1] + mismatchCosts[inputString2[j-1]][inputString1[i-1]],
                memoizedArray1[j-1][i] + delta,
                memoizedArray1[j][i-1] + delta
            )

    #last half of X
    inputString1Reversed, inputString2Reversed = "".join(reversed(inputString1)), "".join(reversed(inputString2))
    string1LenRemainder = string1Len - string1LenDivided
    memoizedArray2 = [[0 for x in range(string1LenRemainder + 1)] for y in range(string2Len + 1)] 

    for i in range(string1LenRemainder + 1):
        memoizedArray2[0][i] = i * delta

    for i in range(string2Len + 1):
        memoizedArray2[i][0] = i * delta
    
    for j in range(1, string2Len + 1):                                               
        for i in range(1, string1LenRemainder + 1):
            memoizedArray2[j][i] = min(
                memoizedArray2[j-1][i-1] + mismatchCosts[inputString2Reversed[j-1]][inputString1Reversed[i-1]],
                memoizedArray2[j-1][i] + delta,
                memoizedArray2[j][i-1] + delta
            )
    
    #add and find min for optimal splitting point (min cost of alignment for split). final col of each array contains opt costs of alignment.
    costOfAlignmentArr = []
    for i in range (string2Len +1): 
        costOfAlignmentArr.append(memoizedArray1[i][string1LenDivided] + memoizedArray2[string2Len-i][string1LenRemainder]) #(k chars of Y) + (n-k chars of Y)
    print(min(costOfAlignmentArr))
    costOfOptimalAlignment = min(costOfAlignmentArr)
    print(costOfAlignmentArr.index(costOfOptimalAlignment))
    optAlignmentY1 = costOfAlignmentArr.index(costOfOptimalAlignment)
    optAlignmentY2 = string2Len - optAlignmentY1

    m, n = string1LenDivided, optAlignmentY1
    alignedString1, alignedString2 = "", ""
    while(m > 0 or n > 0): 
        if memoizedArray1[n][m] == memoizedArray1[n-1][m-1] + mismatchCosts[inputString1[m-1]][inputString2[n-1]]:
            alignedString1 += inputString1[m-1] 
            alignedString2 += inputString2[n-1]
            m -= 1   
            n -= 1
        elif memoizedArray1[n][m] == memoizedArray1[n-1][m] + delta:   #elif memoizedArray[n][m] == memoizedArray[n][m-1] + delta:
            alignedString1 += "_"                                    #alignedString1 += inputString1[m-1]
            alignedString2 += inputString2[n-1]                      #alignedString2 += "_"
            n -= 1                                                   #m -= 1
        else:
            alignedString1 += inputString1[m-1]                      #alignedString1 += "_"
            alignedString2 += "_"                                    #alignedString2 += inputString2[n-1]
            m -= 1                                                   #n -= 1
    firstHalfX = "".join(reversed(alignedString1))
    firstHalfY = "".join(reversed(alignedString2))
    print("first half of X: " + firstHalfX)
    print("first half of Y: " + firstHalfY)


    m, n = string1LenRemainder, optAlignmentY2
    alignedString1, alignedString2 = "", ""
    while(m > 0 or n > 0): 
        if memoizedArray2[n][m] == memoizedArray2[n-1][m-1] + mismatchCosts[inputString1Reversed[m-1]][inputString2Reversed[n-1]]:
            alignedString1 += inputString1Reversed[m-1] 
            alignedString2 += inputString2Reversed[n-1]
            m -= 1   
            n -= 1
        elif memoizedArray2[n][m] == memoizedArray2[n-1][m] + delta:   #elif memoizedArray[n][m] == memoizedArray[n][m-1] + delta:
            alignedString1 += "_"                                    #alignedString1 += inputString1[m-1]
            alignedString2 += inputString2Reversed[n-1]                      #alignedString2 += "_"
            n -= 1                                                   #m -= 1
        else:
            alignedString1 += inputString1Reversed[m-1]                      #alignedString1 += "_"
            alignedString2 += "_"                                    #alignedString2 += inputString2[n-1]
            m -= 1                                                   #n -= 1
    lastHalfX = "".join((alignedString1))       #don't have to reverse bc the array had reversed X and Y already
    lastHalfY = "".join((alignedString2))
    print("last half of X: " + lastHalfX)
    print("last half of Y: " + lastHalfY)

    #conquer - concatenating the string
    print (firstHalfX + lastHalfX)
    print (firstHalfY + lastHalfY)
    
    
    #scrappable code - just to output opt array in a readable form
    
    '''f = open(os.path.join(cwd, "efficientMemoizedArrayOutput"), "w")
    for row in memoizedArray1: 
        f.write(", ".join(str(x) for x in row) + "\n")
    f.close()'''

    