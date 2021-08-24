from __future__ import division
import numpy as np
import sys
import json

totalvar = sys.argv[1]
totalcons = sys.argv[2]
objZ = json.loads(sys.argv[3])
matrix = json.loads(sys.argv[4])
countgreat = sys.argv[5]
type = sys.argv[6]

# totalvar= 2
# totalcons= 3
# objZ= [4, 1]
# matrix= [['3', '1', '=', '3'], ['4', '3', '>=', '6'], ['1', '2', '<=', '4']]
# countgreat= 1
# type= 2

# totalvar= 3
# totalcons= 2
# objZ= [6, -2, 3]
# matrix= [['2', '-1', '2', '<=', '2'], ['1', '0', '4', '<=', '4']]
# countgreat= 0
# type= 1

# totalvar= 2
# totalcons= 2
# objZ= [2, 1]
# matrix= [['3', '4', '<=', '6'], ['6', '1', '<=', '3']]
# countgreat= 0
# type= 1

totalvar = int(totalvar)
totalcons = int(totalcons)
objZ = [int(i) for i in objZ]
countgreat = int(countgreat)
type = int(type)
eqlCount = 0

for i in matrix:
    if '=' in i:
        eqlCount += 1


try:
    M = -9999
    # fun = int(input("Press -> 1-MAX 2-MIN : "))
    fun = type
    #Coefficients of objective function
    # ntemp = int(input("Enter the number of variables : "))
    ntemp = totalvar

    # cinp = list(
    #     map(int, input("Enter coefficients of objective functions : ").split()))
    cinp = objZ
    
    #storing coeff of objective function for later calculation
    objectiveCoeff = cinp

    # constNum = int(input("Enter the number of constraints : "))
    constNum = totalcons

    # gtemp = int(input("Enter the number of >= constraints : "))
    gtemp = countgreat


    if fun == 2:
        cinp = [i * -1 for i in cinp]

    for i in range(constNum - eqlCount):
        cinp.append(0)

    for i in range(gtemp + eqlCount):
        cinp.append(M)

    c = np.array(cinp)

    # objective function ended

    #Coefficients of constraints
    # print("Enter the coefficients of the constraints with inequality sign (Eg. 1 2 <= 4 ) : ")
    constraints = []
    slackptr = ntemp
    size = gtemp + ntemp + constNum

    artptr = ntemp + constNum - eqlCount

    rhsVars = []

    for i in matrix:
        temp = i
        type = temp[-2]
        rhsVars.append(int(temp[-1]))
        temp.pop()
        temp.pop()

        for i in range((gtemp+constNum)):
            temp.append('0')

        for i in range(len(temp)):
            temp[i] = int(temp[i])

        if '<=' == type:
            temp[slackptr] = 1
            slackptr += 1
        elif '>=' == type:
            temp[slackptr] = -1
            temp[artptr] = 1
            slackptr += 1
            artptr += 1
        elif '=' == type:
            temp[artptr] = 1
            artptr += 1

        constraints.append(temp)

    A = np.array(constraints)

    #RHS of inequality

    b = np.array(rhsVars)
    #B contains basic variables that make I matrix

    Bnik = []
    for i in constraints:
        temp = []
        temp.append((i[ntemp: len(i)].index(1))+ntemp)
        Bnik.append(temp)

    B = np.array(Bnik)

    Binv = np.identity(constNum, float)

    # cb contains value of basic variables that make I matrix

    reached = 0  # will turn 1 if optimality reached
    unbounded = 0
    alternate = 0

    while reached == 0:

        #calculate delta j -> zj-cj for non basics
        cj = np.delete(c, B.T[0])
        aj = np.delete(A, B.T[0], 1)

        cb = np.array(c[B.T[0]])  # initially cb = [0,0]
        deltaj = np.dot(np.dot(cb, Binv), aj)-cj

        #check for alternate solution
        for x in deltaj:
            if x == 0:
                alternate = 1

        flag = 0
        for x in deltaj:
            if x < 0:
                flag = 1
                break

        if flag == 0:
            print("Delta j for all j are >= 0, Optimality reached")
            reached = 1
            break
        # kth var will enter the basis
        k = np.argmin(deltaj)
        # X var is entering vector
        X = np.dot(Binv, aj[:, k])
        xb = np.dot(Binv, b)
        xb = xb.astype('float64')
        i = 0
        r = -1
        minimum = 9999
        # minimum ratio test
        while i < len(Binv):
            if(xb[i] >= 0 and X[i] > 0):
                val = xb[i]/X[i]
                if val < minimum:
                    minimum = val
                    r = i  # B[r][0] is the leaving var
            i += 1
        # Unbounded LPP
        if r == -1:
            unbounded = 1
            break
        pivot = X[r]

        #perfroming row operation on pivot row
        for i in range(0, len(Binv)):
            Binv[r][i] /= pivot
        #performing row operation on other rows of Binv

        for i in range(0, len(Binv)):
            if i != r:
                div_factor = X[i]
                for j in range(0, len(Binv)):
                    Binv[i][j] = Binv[i][j] - (div_factor*Binv[r][j])

        #if leaving vector is artificial varibale, then kicking that coloumn form A and c
#         tflag = ntemp + constNum - eqlCount
#         for i in (tflag, len(A)):
#             if(i==B[r][0]):
#                 c = np.delete(c, B[r][0])
#                 A = np.delete(A, B[r][0], 1)
                
        # updating basic variables
        for i in range(0, len(A[0])):
            chk1 = np.array([row[i] for row in A])
            chk2 = aj[:, k]
            if (chk1 == chk2).all():
                B[r][0] = i
        xb = np.dot(Binv, b)

    if(unbounded == 1):
        print("The given LPP is unbounded")
    else:
        finalAns = {}
        infeasible = False
        counterXb = 0

        for i in B:
            finalAns[f"x{i[0]+1}"] = xb[counterXb]
            counterXb += 1

        # print(finalAns)
        Zvalue = 0
        
        for i in range(1, ntemp+1):
            if f"x{i}" in finalAns:
                print( f"x{i}","=",finalAns[f"x{i}"])
                Zvalue += objectiveCoeff[i-1]*finalAns[f"x{i}"] #calculating Z value
            else:
                print(f"x{i} = 0")
                
        print("Z =", Zvalue)

        for i in finalAns:
            if (int(i[1])-1) in range(ntemp+constNum-eqlCount, len(A[0])):
                infeasible = True

        if infeasible:
            print("The given LPP is infeasible")

        if alternate == 1:
            print("Alternate solution also exists for the given LPP")
except:
    print("Invalid Input")
