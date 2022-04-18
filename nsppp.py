# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 16:18:28 2021

@author: Reindolf Ocran Boadu
"""

#Solving the Nurse Scheduling Problem
#Number of nurses
n=20 #This number can be changed
#A list for number of shifts
jj=[1,2,3] #Index of shifts
kk=[1,2,3,4,5,6,7] #index of days
ii=[nurses for nurses in range(n)]
a1=5 #Number of nurses required for morning shift each day
a2=5#Number of nurses required for afternoon shift each day
a3=5 # Number of nurses required for evening shift each day


#Matrix for nurse i preferences for a shift j on day k
f=[1,5,9,9,1,5,9,9]

#Importing the pulp library
import pulp as p
#Creating the Lp Problem with title; "Nurse Scheduling Problem"
model = p.LpProblem("Nurse Scheduling Problem", sense = p.LpMaximize)

#Defining variables
#Which is 1 when nurse i is assigned to shift j on day k, 0 otherwise
x = p.LpVariable.dicts("x", [ (i, j, k) for i in ii
                                            for j in jj
                                            for k in kk], 0, 1, 'Binary')

#objective function
#Our objective is to maximize the nurse's preferences for a shift j on a day k
    
model += p.lpSum(f[k] * x[(i, j, k)]
                 for k in kk
                 for j in jj
                 for i in ii
                 )

#Constraint 1
#Each nurse must be scheduled for at most one shift each day
for i in ii:
    for k in kk:
        
        model += p.lpSum(x[(i, j, k)] for j in jj
                      ) <= 1


#Constraint 2
#No nurse may be scheduled to work a night shift followed immediately by a morning shift
for k in range(1,len(kk)):
    for i in ii:
        model += x[(i, 3, k)] + x[(i, 1, k+1)] <= 1

#Constraint 3
#Each nurse must have at least one day-off in the planning horizon
for i in ii:
    model += p.lpSum(x[(i, j, k)]
                     for j in jj
                     for k in kk) <= 6

#.........................................................................
#Constraint 4
#Nurses assigned each morning should be equal to the number of nurses 
#needed for morning
#shifts each day which we assume to be constant for all the days
for k in kk:
    
    model += p.lpSum(x[(i, 1, k)] for i in ii) == a1

#Constraint 5
#Nurses assigned each afternoon should be equal to the number of 
#nurses needed for a afternoon
#shift each day which we assume to be constant for all the days
for k in kk:
    
    model += p.lpSum(x[(i, 2, k)] for i in ii) == a2

#Constraint 6
#Nurses assigned each morning should be equal to the number of nurses 
#needed for an evening
#shift each day which we assume to be constant for all the days
for k in kk:
    
    model += p.lpSum(x[(i, 3, k)] for i in ii) == a3

#.....................................................................................
#More constraints

#Constraint 7
#Each nurse is not assigned more than two consecutive morning shifts
for k in range(1,len(kk)-1):
    for i in ii:
        model += x[(i, 1, k)] + x[(i, 1, k+1)] + x[(i, 1, k+1)] <= 2

#Constraint 8
#Each nurse is not assigned more than two consecutive afternoon shifts
for k in range(1,len(kk)-1):
    for i in ii:
        model += x[(i, 2, k)] + x[(i, 2, k+1)] + x[(i, 2, k+1)] <= 2

#Constraint 9
#Each nurse is not assigned more than two consecutive evening shifts
for k in range(1,len(kk)-1):
    for i in ii:
        model += x[(i, 3, k)] + x[(i, 3, k+1)] + x[(i, 3, k+1)] <= 2


#Constraint 10
#Maximum of three night shifts for a nurse for each planning horizon

for i in ii:
    model += p.lpSum(x[(i, 3, k)]
                         for k in kk) <= 3




#Solution
soln=model.solve()

#Generating the status of the solution
print("The solution has a status of", soln)
print("This implies that it is", p.LpStatus[model.status])
print('')
f=open("C:/Users/USER/Desktop/Schedule2.txt","a+")
#Printing the values for each decision variable
print("The values of the decision variables are: ")
for var in x:
    var_value=x[var].varValue
    print(x[var],"=" ,var_value)
    hello=str(x[var]) + "=" +str(var_value)
    f.write(str(hello)+"\n")

#Printing the vaule of the objective
obj=model.objective.value()
print('')
print('The cost of the scheduling is', obj)
f.close()

