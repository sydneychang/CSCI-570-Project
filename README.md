# CSCI-570-Project: Sequence Alignment Problem
Basic + Memory Efficient Implementations
Using Python3

# TO-DO
**input string generator...create a string for the actual algorithm**
- assume valid string and integer input (ACTG only and non negative/within bounds of string)
- same for basic/efficient versions
- use the same method in the respective files (basic_3.py and efficient_3.py)
- j does NOT have to equal k!!!!
- should read from an input file.
- needs to output results into a separate file


**basic version**
- hardcode gap penalty (delta) & mismatch costs (alpha) - dict of dicts
- bottom up pass: 
    - initialize first column and row based on deltas * string length (these are the costs if a given string must be aligned with an empty string)
    - use the recurrence formula to fill out the values row by row, column by column
    - the value of the optimal solution should be at memorizedArray[n][m]
- top down pass: 
    - sneaky gotchas:
        - while loop should be "or" not "and". even if the alignment reaches the 0th column, it should continue down the rows as it needs to iterate back down to 0, 0 (and vice versa).
        - it's ROW BY COLUMN...when accessing memorizedArray[n][m]
        - order of if statements matter in the final alignment!! kept the alternate ordering of if statements to compare easily with outputs. note that these alignments are of the same cost and therefore equivalent
    - started from memorizedArray[n][m] and obtained the sequence, iterating through the array back to [0][0]
    - reversed the string to get the result

**memory efficient version**
- divide and conquer
- black magic???

**output file**
- cost of alignment (int)
- first string alignment (ACTG_)
- second string alignment (ACTG_)
- time in ms (float) 
    - refer to code pg 10 of specs
- memory in kb (float)
    - refer to code pg 10 of specs

**report graph && summary.docx analysis**
- run the 2 algorithms on the 15 input files in "datapoints" folder. Make 2 graphs:
    - 1 plot for CPU time vs problem size for both solutions
        - iirc, the CPU time should be the same for both solutions
            - X-axis = problem size, m+n (length of input strings). 
            - Y-axis = CPU time, ms.
        - 1 plot for Memory usage vs problem size for 2 solutions
            - X-axis = problem size, m+n (length of input strings). 
            - Y-axis = Memory Usage, KB.
- fill out the summary.docx
- don't have to provide the code for making the plots. Just images. 
    
**shell files**
- ??? think this is just command console scripts 

**submission**
- double check file structure/naming format




