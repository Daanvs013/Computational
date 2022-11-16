## group 5
## Daan van Turnhout 2051976
## Freek
## Julia van Lieshout
## Bram van der Kleij

## modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from classes import BrownianMotion, GeometricBrownianMotion, ItoDiffusionEuler, BlackScholesOptionPrice, SolvePDEBoundaryNumerically
## set seeds
np.random.seed(5)
seed = 5

## question 1
sigma = 1
n = 1000
t=3
time_step = 10**(-3)
sbm = BrownianMotion(sigma,n,t,time_step,seed=seed)
##sbm.plot()
##plt.show()

## question 1a
def V(i: int,p: int, t:int):
    f = lambda x: x**2

    value = 0
    n = t*10**i
    for k in range(1,n+1):
        tk = k*10**(-i)
        value += abs(f(tk) - f(tk-1))**p
    return value

def Q1a():
    t = 3
    i = [1,2,3]
    p = [1,2]
    for element in i:
        for element2  in p:
            value = V(element,element2,t)
            print(f"i={element}, p={element2}, V={value}")
##Q1a()

## question 1b
def FV(i,process):
    value = 0
    n = 3*10**i
    for k in range(1,n+1):
        value += abs( process[k] - process[k-1])
    return value

def RV(i,process):
    value = 0
    n = 3*10**i
    for k in range(1,n+1):
        value += ( process[k] - process[k-1])**2
    return value

def Q1b():
    i = [1,2,3]

    for el in i:
        fv = []
        rv = []
        for path in sbm.paths:
            fv.append(FV(el,path))
            rv.append(RV(el,path))
        fv = np.array(fv)
        rv = np.array(rv)
        fv_mean = np.mean(fv)
        rv_mean = np.mean(rv)
        fv_std = np.std(fv)
        rv_std = np.std(rv)
        print(f"i = {el}, FV: mean={fv_mean}, var={fv_std**2}, RV: mean={rv_mean}, var={rv_std**2}")
        ## plot
        plt.figure(f"Q1b i={el} FV")
        plt.hist(fv)
        plt.xlabel("FV")
        plt.title(f"Histogram for realisations of FV when i={el}")
        plt.figure(f"Q1b i={el} RV")
        plt.hist(rv)
        plt.xlabel("RV")
        plt.title(f"Histogram for realisations of RV when i={el}")
    plt.show()
#Q1b()

## Exercise 1c
def Q1c():

    ## exact simulation
    s0 =100
    mu = 0.08
    sigma = 0.3
    ## same grid as sbm so:
    n = 1000
    t= 3
    stepsize = 10**(-3)
    ## by using the same seed and grid, we are using essentially the sbm we created in Q1a
    stock_exact = GeometricBrownianMotion(s0,mu,sigma,n,t,stepsize,seed=seed)
    stock_exact.plot(5)
    plt.title(f"Exact simulation for the stock price")
    plt.ylabel("Stock price")
    plt.xlabel("time")
    
    ## euler approx.
    i= [1,2,3]
    for el in i:
        drift = lambda t,x: mu*x
        volatility = lambda t,x: sigma*x
        time_step = 10**(-el)
        ## again, by using the same seed and grid, we are using essentially the sbm we created in Q1a
        stock_euler = ItoDiffusionEuler(s0,drift,volatility,n,t,time_step,seed=seed)
        stock_euler.plot(5)
        plt.title(f"Euler Approx. for the stock price with i={el}")
        plt.ylabel("Stock price")
        plt.xlabel("time")
    plt.show()
#Q1c()

## Exercise 1d


## Exercise 1e
def approx_integral(i,sigma,process):
    n = 3*10**i
    value = 0
    for k in range(1,n+1):
        value += (sigma**2)*(process[k-1]**2)*10**(-i)
    return value

def Q1e():
    ## exact simulation
    s0 =100
    mu = 0.08
    sigma = 0.3
    ## same grid as sbm so:
    n = 1000
    t= 3
    stepsize = 10**(-3)
    ## by using the same seed and grid, we are using essentially the sbm we created in Q1a
    stock = GeometricBrownianMotion(s0,mu,sigma,n,t,stepsize,seed=seed)

    i = [1,2,3]
    for el in i:
        rv = []
        aprox = []
        for path in stock.paths:
            rv.append(RV(el,path))
            aprox.append(approx_integral(el,sigma,path))
        rv = np.array(rv)
        aprox = np.array(aprox)

        value = rv-aprox

        value_mean = np.mean(value)
        value_std = np.std(value)
        print(f"i = {el}, RV_S - [S,S]_T: mean={value_mean}, var={value_std**2}")
        ## plot
        plt.figure(f"Q1e i={el}")
        plt.hist(aprox)
        plt.xlabel("Y")
        plt.title(f"Histogram for realisations of Y for i={el}")
    plt.show()
#Q1e()  


## Exercise 3a
def Q3a():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01
    t=1
    option = BlackScholesOptionPrice(k,r,sigma)
    price = option.price_put(s0,t)
    print(f"Price of put option: {price}")
Q3a()

## Exercise 3b
def Q3b():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01
    t=1

    smax = 250
    ds = 0.01
    dt = 0.01
    bound_t = lambda s: np.maximum(k-s,0)
    bound_smax = lambda t: 0

    option = SolvePDEBoundaryNumerically(smax,ds,k,dt,t,r,sigma,bound_t,bound_smax)
    price = option.price_specific_point(0,s0)
Q3b()