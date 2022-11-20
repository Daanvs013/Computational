# -*- coding: utf-8 -*-
"""
Group number: 21
Members:
    1. Daan Spanbroek
    2. Daan van Turnhout 2051976
    3. Dico de Gier
    4. Hendrik Verkaik
"""

## modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
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
#Q1b()

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
#print(Q1f())
"""
Exercise 1g)
"""
def Q1g():
    a = 0
    b = 5
    ## generate the p values with stepsize 0.001
    p = np.arange(a,b,0.001)
    ## generate samples
    samples = generate([a],[b],len(p))
    y = []
    ## calculate the corresponding revenue for each pi
    for i in p:
        y.append(estimate_revenue(i,samples))
    ## plot
    plt.figure(f"Q1g: plot on [{a},{b}]")
    plt.plot(p,y)
    plt.xlim(a,b)
    plt.xlabel("p")
    plt.ylabel("Estimated Revenue")
    plt.title(f"Estimated Revenue plot on [{a},{b}]")
    ## determine optimal value for p
    opt = getOptSamples([a],[b],samples)
    ## because we flipped the sign, we need to flip it back to obtain the correct func value at the optimal p
    plt.scatter(opt.get("x"), -1*opt.get("fun"))
    plt.show()
#Q1g()

"""
Exercise 1h)
"""
def matching(p:list,v:list):
    p = np.array(p)
    v = np.array(v) ## assume that buyer always has a value assigned to a item. vi >= 0 for all items
    ## subtract pi from vi for all j buyers
    weight = v-p
    ## set all negative weights to zero
    weight[weight<0] = 0
    ## optimize
    row_ind,col_ind = optimize.linear_sum_assignment(weight, maximize=True)
    ## row contains buyers as index of the weight matrix
    ## col contains the corresponding items as index of weight matrix

    ## create helper arrays that will hold the matchings after filtering out the non-positive weights
    row = np.array([], dtype='int64')
    col = np.array([], dtype='int64')

    ## loop through the buyers
    for it in range(0,len(row_ind)-1):
        j = row_ind[it]
        ## get the corresponding item according to the optimzer
        i = col_ind[it]
        ## get the corresponding weight
        cost = weight[i,j] 
        ## add the row,col indice to the helper arrays if the matching weight is positive (Vij > Pi for buyer j to buy item i)
        if cost > 0:
            row = np.append(row,i)
            col = np.append(col,j)
    ## calculate the total sum of prices
    total = weight[row,col].sum()
    ## output
    return row,col,total
"""
p = [0.1,0.6]
v = [[0.04872488080912729, 0.28910965978981684], [0.7209663468312298, 0.021616249915949792]]
print(matching(p,v))
#"""

"""
Exercise 1i)
"""
def average_price(p:list,n:int,K:int):
    p = np.array(p)
    m = len(p)
    tot = 0
    ## perform K iterations
    for it in range(0,K):
        ## generate value V matrix
        v = []
        ## for every buyer, generate values for m items
        for j in range(0,n):
            values = generate([0],[1],m)
            v.append(values)
        ## matching
        row,col,total = matching(p,v)
        tot += total
    
    ## calculate average
    avg_price = tot/K
    return avg_price

"""
Exercise 1j)
"""
def Q1j(m:int,n:int,K:int,delta:int):
    ## generate ki
    k = np.arange(0,delta+1,1)
    p_delta = []
    ## generate K times the vector p which contains m amount of prices
    for j in range(0,K):
        ## generate p
        p = []
        for i in range(0,m):
            pi = k[i]/delta
            p.append(pi)
        p_delta.append(p)

    ## calculate optimum wrt the given set p_delta
    opt = {"p":[],"avg_price":0}

    for i in p_delta:
        avg = average_price(i,n,K)
        if avg > opt['avg_price']:
            opt["p"] = i
            opt['avg_price'] = avg
        else:
            pass
    
    return opt

"""
Exercise 1k)
"""
def Q1k():
    m = 2
    n = 3
    K = 100
    delta = 50
    result = Q1j(m,n,K,delta)
    print(result)
Q1k()

