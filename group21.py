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
    ## X is continuous random variable
    ## X~UNIF(a,b)
    cdf = lambda x: (x-a)/(b-a)
    pdf = 1/(b-a)
    ## we know P[X<p] = cdf(p)
    ## revenue = p * P[X>p] = p * (1-P[X<p])
    r = p * (1-cdf(p))
    return r

def getOptP(a,b):
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
    ## if list is a sample from unif then this function represents the estimate for the revenue
    list = np.array(list)
    n = len(list)
    frac = len(list[list>p])/n
    return p*frac

"""
Exercise 1e)
"""
def getOptSamples(a:list,b:list,t:list):
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
    ## please see the report for an explanation of the output of this function
    for i in range(0,len(p)):
        for j in range(0,np.shape(V)[1]):
            if p[i] >= V[i][j]:
                V[i][j] = 0
            else:
                V[i][j] = p[i]

    V = V*-1
    row_ind, col_ind = optimize.linear_sum_assignment(V)
    value = 0
    row = np.array([], dtype='int64')
    col = np.array([], dtype='int64')
    for i in range(len(row_ind)):
        if V[i][col_ind[i]] != 0:
            row = np.append(row,i)
            col = np.append(col,col_ind[i])
            value += V[i][col_ind[i]]
    
    value = value*-1
    return [row, col, value]

"""
Exercise 1i)
"""
def average(p,n,K):
    counter = 0
    total = 0
    np.random.seed(21)
    while counter < K:
        m = len(p)
        V = np.random.rand(m,n)
        total += matching(p,V)[2]
        counter += 1
    return total/K

"""
Exercise 1j)
"""
def grid(m,n,delta,K):
    vector = np.linspace(0,1,delta+1)
    max = [0,0]
    for x in it.product(vector,repeat=m):
        y = np.array(x) #it.product returns a tuple
        result = [average(y,n,K), y]
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

