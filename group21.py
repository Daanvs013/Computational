# -*- coding: utf-8 -*-
"""
Group number: 21
Members:
    1. Daan Spanbroek 2056711
    2. Daan van Turnhout 2051976
    3. Dico de Gier 2058017
    4. Hendrik Verkaik 2053998
"""

## modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import itertools as it

np.random.seed(21)

"""
Exercise 1a)
"""
def revenue(p,a,b):
    """returns expected revenue"""
    ## X is continuous random variable
    ## X~UNIF(a,b)
    cdf = lambda x: (x-a)/(b-a)
    pdf = 1/(b-a)
    ## we know P[X<p] = cdf(p)
    ## revenue = p * P[X>p] = p * (1-P[X<p])
    r = p * (1-cdf(p))
    return r

def getOptP(a,b):
    """returns optimized revenue"""
    ## max f = min -f
    ## we want to maximize, so flip sign of the function revenue()
    f = lambda p,a,b: -revenue(p,a,b)
    x0 = a
    result = optimize.minimize(f,x0,args=(a,b))
    return result

"""
Exercise 1b)
"""
def Q1b():
    """returns plots of expected revenue and the maximum for the values in list"""
    list = [(0,1),(10,20),(20,60),(40,100)]
    for pair in list:
        a = pair[0]
        b = pair[1]
        ## generate the p values with step 0.01
        p = np.arange(a,b,0.01)
        y = revenue(p,a,b)
        ## plot
        plt.figure(f"Q1b: Plot on [{a},{b}]")
        plt.plot(p,y)
        plt.xlim(a,b)
        plt.xlabel("p")
        plt.ylabel("Expected Revenue")
        plt.title(f"Revenue plot on [{a},{b}]")
        opt = getOptP(a,b)
        ## because we flipped the sign, we need to flip it back to obtain the correct func value at the optimal p
        plt.scatter(opt.get("x"), -1*opt.get("fun"))
    plt.show()
Q1b()

"""
Exercise 1c)
"""
def generate(a:list,b:list,t:int):
    """returns t samples"""
    ## check if a and b have the same length
    if len(a) == len(b):
        output = []
        ## take t amount of samples
        for k in range(0,t):
            y = 0
            ## for each t, take len(a) times a random variable and sum it up
            for i in range(0,len(a)):
                x = np.random.uniform(a[i],b[i])
                y += x
            output.append(y)
        return output
    else:
        print("a and b must be the same length")
        
"""
Exercise 1d)
"""
def estimate_revenue(p,list):
    """returns p times the fraction of numbers that are greater or equal than p"""
    ## if list is a sample from unif then this function represents the estimate for the revenue
    list = np.array(list)
    n = len(list)
    frac = len(list[list>p])/n
    return p*frac

"""
Exercise 1e)
"""
def getOptSamples(a:list,b:list,t:list):
    """returns optimized result of question 1d)"""
    ## max f = min -f
    ## we want to maximize, so flip sign of the function in (d)
    f = lambda p,t: -estimate_revenue(p,t)
    x0 = sum(a)
    result = optimize.minimize(f,x0, args=(t), method="Nelder-Mead")
    return result

"""
Exercise 1f)
"""
def Q1f():
    a = [0,0,1]
    b = [1,2,2]
    t = 1000
    ## generate t amount of samples
    samples = generate(a,b,t)
    ## get the maximum using question (e)
    result = getOptSamples(a,b, samples)
    ## note to interpret: flip sign of result.get('fun'), because we minimized -f
    return result
print(Q1f())
"""
Exercise 1g)
"""
def Q1g():
    """returns plot of revenue with maximum""" 
    a = [0,0,1]
    b = [1,2,2]
    ## generate the p values with stepsize 0.001
    p = np.arange(0,5,0.001)
    ## generate samples
    samples = generate(a,b,len(p))
    y = []
    ## calculate the corresponding revenue for each pi
    for i in p:
        y.append(estimate_revenue(i,samples))
    ## plot
    plt.figure(f"Q1g: plot on [0,5]")
    plt.plot(p,y)
    plt.xlim(0,5)
    plt.xlabel("p")
    plt.ylabel("Estimated Revenue")
    plt.title(f"Estimated Revenue plot on [0,5]")
    ## determine optimal value for p
    opt = getOptSamples(a,b,samples)
    ## because we flipped the sign, we need to flip it back to obtain the correct func value at the optimal p
    plt.scatter(opt.get("x"), -1*opt.get("fun"))
    plt.show()
Q1g()

"""
Exercise 1h)
"""
def matching(p,V):
    """returns row indices and column indices of maximum matching, along with the value of the maximum matching"""
    ## please see the report for a step-by-step guide through this function and a detailed explanation of the output
    for i in range(0,len(p)):
        for j in range(0,np.shape(V)[1]):
            if p[i] >= V[i][j]: ##if price exceeds value, entry of the matrix should get value 0 in the matching
                V[i][j] = 0
            else:
                V[i][j] = p[i] ##otherwise, the entry of the matrix should get the value of the price in the matching

    V = V*-1
    row_ind, col_ind = optimize.linear_sum_assignment(V)
    value = 0
    ##create arrays to store final matching
    row = np.array([], dtype='int64')
    col = np.array([], dtype='int64')
    for i in range(len(row_ind)):
        if V[i][col_ind[i]] != 0: ##only entries with a value unequal to zero should appear in the final matching
            row = np.append(row,i)
            col = np.append(col,col_ind[i])
            value += V[i][col_ind[i]]
    
    value = value*-1
    return [row, col, value]

"""
Exercise 1i)
"""
def average(p,n,K):
    """returns average value of the maximum matching with K runs"""
    counter = 0
    total = 0
    np.random.seed(21) ##we again set the seed to 21 to make sure that we can accurately compare the values
    while counter < K:
        m = len(p)
        V = np.random.rand(m,n) ##create random matrix with size mxn
        total += matching(p,V)[2]
        counter += 1
    return total/K

"""
Exercise 1j)
"""
def grid(m,n,delta,K):
    """returns maximum value and optimal price vector"""
    vector = np.linspace(0,1,delta+1) ##all possible values of p_i
    max = [0,0]
    for x in it.product(vector,repeat=m): ##will cover every possible combination of p
        y = np.array(x) #it.product returns a tuple
        result = [average(y,n,K), y] ##for each possible vector of p, we apply the average function K times
        if result[0] > max[0]:
            max = result
    return "Max value {} is achieved at price vector {}".format(max[0], max[1])

"""
Exercise 1k)
"""
def Q1k():
    m = 2
    n = 3
    K = 100
    delta = 50
    result = grid(m,n,delta,K)
    print(result)
Q1k()

