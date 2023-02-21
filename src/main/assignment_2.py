import numpy

numpy.set_printoptions(precision=7, suppress=True, linewidth=100)

def nevilles(xVals, yVals, x):
    matrix = numpy.zeros((len(xVals), len(yVals)))

    #copy over the Ys into the first column of the matrix
    c = 0
    for i in matrix:
        matrix[c][0] = yVals[c]
        c = c+1
    
    # y1 0  0  
    # y2 0  0   Should look roughly like this at this point
    # y3 0  0  
    # . . . . . 

    count1 = 0
    count2 = 0
    for i in matrix:
        if count1 > 0:
            for j in matrix:
                if (count2 > 0) and (count2 <= count1):
                    xStart = xVals[count1-count2] #Basically X0 for most equations
                    xEnd = xVals[count1] #Basically X1
                    formula1 = (1/(xEnd-xStart))
                    formula2 = ((x-xStart)*matrix[count1][count2-1])-((x-xEnd)*matrix[count1-1][count2-1])
                    finalForm = formula1*formula2
                    matrix[count1][count2] = finalForm
                count2 = count2 + 1
        count1 = count1 + 1
        count2 = 0
    print(matrix[count1-1][count2-1])
    print("")


def newtons(xVals, yVals, x):
    matrix = numpy.zeros((len(xVals), len(yVals)))

    #copy over the Ys into the first column of the matrix
    c = 0
    for i in matrix:
        matrix[c][0] = yVals[c]
        c = c+1
    
    # y1 0  0  
    # y2 0  0   Should look roughly like this at this point
    # y3 0  0  
    # . . . . . 

    count1 = 0
    count2 = 0
    coeffs = numpy.zeros((len(xVals)-1, 3))
    coeffsFin = numpy.zeros(len(xVals)-1)
    for i in matrix:
        if count1 < 3:
            coeffs[count1][2] = x-xVals[count1]
            #Stores x Diffs for future use
        if count1 > 0:
            for j in matrix:
                if (count2 > 0) and (count2 <= count1):
                    xStart = xVals[count1-count2] #Basically X0 for most equations
                    xEnd = xVals[count1] #Basically X1
                    formula1 = matrix[count1][count2-1]-matrix[count1-1][count2-1]
                    formula2 = xEnd- xStart
                    finalForm = formula1/formula2
                    matrix[count1][count2] = finalForm
                    #Begin calculating P0, P1,...
                    if count1 == count2:
                        coeffsFin[count1-1] = finalForm
                        #if count1 == 1:
                        #    coeffsFin[0] = matrix[0][0] + matrix[count1][count2]*coeffs[count1-1][2]
                        #elif count1 == 2:
                        #    coeffsFin[1] = coeffs[count1-2][1] + matrix[count1][count2]*coeffs[count1-1][2]*coeffs[count1-2][2]
                        #elif count1 == 3:
                        #    coeffsFin[2] = coeffs[count1-2][1] + matrix[count1][count2]*coeffs[count1-1][2]*coeffs[count1-2][2]*coeffs[count1-3][2]
                count2 = count2 + 1
        count1 = count1 + 1
        count2 = 0
    print(coeffsFin)
    print("")


def hermite(xVals, yVals, slopes):
    matrix = numpy.zeros((2*len(xVals), 2*len(yVals)))
    c1 = 0
    c2 = 0

    #Fill in X Values
    for i in range(0,3):
        matrix[c1][0] = xVals[c2]
        matrix[c1+1][0] = xVals[c2]
        c1 = c1+2
        c2 = c2+1

    #Fill in Y Values
    c1 = 0
    c2 = 0

    for i in range(0,3):
        matrix[c1][1] = yVals[c2]
        matrix[c1+1][1] = yVals[c2]
        c1 = c1+2
        c2 = c2+1
    
    #Fill in Slopes
    c1 = 1
    c2 = 0
    for i in range(1,4):
        matrix[c1][2] = slopes[c2]
        c1 = c1+2
        c2 = c2+1
    
    c1 = 2
    
    for i in range(0,4):
        c2 = 1
        for j in range(0,5):
            if matrix[c1][c2] == 0 and c2 < c1+2:
                

                matrix[c1][c2] = 5
                form1   =  matrix[c1][c2-1] - matrix[c1-1][c2-1]
                form2   =  matrix[c1][0] - matrix[c1-(c2-1)][0]
                formFin =  form1/form2

                matrix[c1][c2] = formFin
            c2 = c2+1
        c1 = c1+1
    print(matrix)
    print("")

def cubic(xVals, yVals):
    matrix = numpy.zeros((len(xVals), len(xVals)))
    dataMatrix = numpy.zeros((len(xVals), len(yVals)))
    N = (len(xVals)-1)

    #Assigning Xvals to storage matrix
    c1 = 0
    for i in dataMatrix:
        dataMatrix[c1][0] = xVals[c1]
        c1 = c1+1

    #calulating h's and adding to storage matrix
    c1 = 1
    for i in range(0, 3):
        dataMatrix[c1][1] = dataMatrix[c1][0] - dataMatrix[c1-1][0]
        c1 = c1+1

    #Assignming yVals (a's) into storage matrix
    c1 = 0
    for i in dataMatrix:
        dataMatrix[c1][2] = yVals[c1]
        c1 = c1+1
    
    
    matrix[0][0] = 1
    matrix[3][3] = 1

    c1 = 1
    c2 = 0
    for i in range(0, 3):
        c2 = 0
        for j in matrix:
            if c1 == c2:
                if c1 < N: #keeps us in our reasonable bounds
                    #Diagonal
                    matrix[c1][c2] = 2*((dataMatrix[c1][1]+dataMatrix[c1+1][1]))

                    #Below Diagonal
                    matrix[c1][c2-1] = dataMatrix[c1][1]

                    #Above Diagonal
                    matrix[c1][c2+1] = dataMatrix[c1+1][1]

            c2 = c2+1
        c1 = c1+1

    vectorB = numpy.zeros((N+1))
    c1 = 1
    for i in range(1, N):
        form1   = (3/dataMatrix[c1+1][1])*(dataMatrix[c1+1][2]-dataMatrix[c1][2])
        form2   = (3/dataMatrix[c1][1])*(dataMatrix[c1][2]-dataMatrix[c1-1][2])
        formFin = form1-form2
        vectorB[c1] = formFin
        c1 = c1+1
    
    #best calculated manually
    #| 1  0  0  0 | |0| 
    #| 3  12 3  0 | |0| 
    #| 0  3  10 2 | |1| 
    #| 0  0  0  1 | |0| 
    x1 = 0
    x2 = 36/1332
    x3 = 12/111
    x4 = 0
    vectorX = [x1, x2, x3, x4]


    print(matrix)
    print("")
    print(vectorB)
    print("")
    print(vectorX)



    
    
#MAIN BODY
#FOR NEVILLES METHOD
x_Values = [3.6, 3.8, 3.9]
y_Values = [1.675, 1.436, 1.318]
calcVal = 3.7
nevilles(x_Values, y_Values, calcVal)

#FOR NEWTONS FORWARD METHOD
x_Values = [7.2, 7.4, 7.5, 7.6]
y_Values = [23.5492, 25.3913, 26.8224, 27.4589]
calcVal = 7.3
newtons(x_Values, y_Values, calcVal)
nevilles(x_Values, y_Values, calcVal)

#HERMITES THING
x_Values = [3.6, 3.8, 3.9]
y_Values = [1.675, 1.436, 1.318]
slopes   = [-1.195, -1.188, -1.182]
hermite(x_Values, y_Values, slopes)

#CUBIC SPLINES
x_Values = [2, 5, 8, 10]
y_Values = [3, 5, 7, 9]
cubic(x_Values, y_Values)
