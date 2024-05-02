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
    
    memoizedArray = [[0 for x in range(string1Len + 1)] for y in range(string2Len + 1)]      #x = string1 length, y = string2 length
    
    for i in range(string1Len + 1):
        memoizedArray[0][i] = i * delta

    for i in range(string2Len + 1):
        memoizedArray[i][0] = i * delta