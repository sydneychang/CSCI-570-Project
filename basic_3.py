import os
cwd = os.path.dirname(os.path.abspath(__file__))

def inputStringGenerator() -> list:           #reads from txt file and creates the 2 strings of input for sequence alignment
    count = 0
    inputString1 = ''
    inputString2 = ''
    with open(os.path.join(cwd, 'SampleTestCases', 'input1.txt'), 'r', encoding='UTF-8') as file:
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

    print(inputs[0] + "\n" + inputs[1])
    


