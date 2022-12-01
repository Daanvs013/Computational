## group 5
## Daan van Turnhout 2051976
## Freek
## Julia van Lieshout
## Bram van der Kleij

## modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sc
from classes import *
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
#Q1a()

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

## Exercise 2a
def Q2a():
    years = 4
    t = years
    aex = pd.read_csv("aex.csv").tail(years*365)
    print(aex)

    start_value = aex.iloc[0,1]
    ## mu and sigma in percentage of starting value
    mu = aex["AEX-INDEX"].mean() / (start_value * years)
    sigma = aex["AEX-INDEX"].std() / (start_value * years)
    n = 1000
    time_step= 0.001
    index = GeometricBrownianMotion(start_value,mu,sigma,n,t,time_step,seed=seed)
    index.plot(5)
    plt.title(f"Sample paths of the simulated AEX")
    plt.ylabel("AEX-INDEX")
    plt.xlabel("time")
    plt.show()
#Q2a()

## Exercise 3a
def Q3a():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01
    t=1
    option = BlackScholesOptionPrice(k,r,sigma)
    price = option.price_call(s0,t)
    print(f"Price of call option: {price}")
#Q3a()

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
    bound_t = lambda s: np.maximum(s-k,0)
    bound_smax = lambda t: 0

    option = SolvePDEBoundaryNumerically(smax,ds,k,dt,t,r,sigma,bound_t,bound_smax)
    price = option.price_specific_point(0,s0)
    option.plot_price()
    plt.show()
    print(f"Price call option numerical: {price}")
#Q3b()

def plotSmax():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01
    t=1

    ds = 0.01
    dt = 0.01
    bound_t = lambda s: np.maximum(s-k,0)
    bound_smax = lambda t: 0

    option_price = lambda smax : SolvePDEBoundaryNumerically(smax,ds,k,dt,t,r,sigma,bound_t,bound_smax)

    ## plot smax tegen de call option price at t=0
    x = np.arange(90,300,1)
    y = []
    for i in x:
        print(f"Iteration {i}.",end='\r')
        call = option_price(i)
        y.append(call.price_specific_point(0,s0))
    
    plt.figure("Q3bSmax")
    plt.title("Effect of Smax on the price of the call option")
    plt.xlabel("Smax")
    plt.ylabel("Price of the call option at t=0")
    plt.plot(x,y)
    plt.show()

def plotds():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01
    t=1

    smax = 250
    dt = 0.01
    bound_t = lambda s: np.maximum(s-k,0)
    bound_smax = lambda t: 0

    option_price = lambda ds : SolvePDEBoundaryNumerically(smax,ds,k,dt,t,r,sigma,bound_t,bound_smax)

    ## plot smax tegen de call option price at t=0
    x = np.arange(0.01,1,0.01)
    y = []
    for i in x:
        print(f"Iteration {i}.",end='\r')
        call = option_price(i)
        y.append(call.price_specific_point(0,s0))
    
    plt.figure("Q3bds")
    plt.title("Effect of ds on the price of the call option")
    plt.xlabel("ds")
    plt.ylabel("Price of the call option at t=0")
    plt.plot(x,y)
    plt.show()

def plotdt():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01
    t=1

    smax = 250
    ds = 0.01
    bound_t = lambda s: np.maximum(s-k,0)
    bound_smax = lambda t: 0

    option_price = lambda dt : SolvePDEBoundaryNumerically(smax,ds,k,dt,t,r,sigma,bound_t,bound_smax)

    ## plot smax tegen de call option price at t=0
    x = np.arange(0.01,1,0.01)
    y = []
    for i in x:
        print(f"Iteration {i}.",end='\r')
        call = option_price(i)
        y.append(call.price_specific_point(0,s0))
    
    plt.figure("Q3bdt")
    plt.title("Effect of dt on the price of the call option")
    plt.xlabel("dt")
    plt.ylabel("Price of the call option at t=0")
    plt.plot(x,y)
    plt.show()

## Exercise 3c
def Q3ci():
    k= 105
    s0 = 100
    mu = 0.08
    sigma = 0.2
    r = 0.01

    t = np.arange(0.01,10.01,0.01)
    prices = []
    for maturity in t:
        option = BlackScholesOptionPrice(k,r,sigma)
        price = option.price_call(s0,maturity)
        prices.append(price)

    mean = np.mean(prices)
    print(f"mean of the prices: {mean}")
    ci = sc.stats.t.interval(confidence=0.95, df=len(prices)-1,loc=mean,scale=sc.stats.sem(prices))
    print(f"95% CI for the mean : {ci}")
    ## plot
    plt.figure(f"Q3ci")
    plt.hist(prices, bins=20)
    plt.xlabel("Price")
    plt.title(f"Histogram for the prices of the call option with timestep=0.01")
    plt.show()
#Q3ci()

## Question 4a
def Q4a():
    mu = 0.08
    sigma = 0.2
    s0 = 100
    b0 = 1
    r = 0.02
    k =100
    t = 1

    ## call option
    option = BlackScholesOptionPrice(k,r,sigma)
    delta = option.delta_call(s0,t)
    print(f"Delta of the call option: {delta}")
#Q4a()

def Q4ci():
    mu = 0.08
    sigma = 0.2
    s0 = 100
    b0 = 1
    r = 0.02
    k =100
    t = 1
    num_time_steps_per_unit_of_time = 250
    num_puts = 1000

    time, S, B, phi, psi, price_puts, total_portfolio_value = writing_put_option_delta_hedge_discrete_time(k, t, s0, mu, sigma,b0, r, num_time_steps_per_unit_of_time, num_puts)
    df = pd.DataFrame(data = np.array([time, S, B, phi, psi, price_puts, total_portfolio_value]).T, columns=["t", "S", "B","position S", "position B", "num_puts * put_price", "total_portfolio_value"])
    fig, ax = plt.subplots(2, 3, figsize=(25, 10))
    df.plot(x="t", y="B", title="path B", ax=ax[0, 0])
    df.plot(x="t", y="S", title="path S (red=strike puts)", ax=ax[0, 1])
    ax[0, 1].axhline(y=k, color="r")
    df.plot(x="t", y="num_puts * put_price", title=f"value {num_puts} puts", ax=ax[0, 2])
    df.iloc[:-1].plot(x="t", y="position B", title="path psi (position B)", ax=ax[1, 0])
    df.iloc[:-1].plot(x="t", y="position S", title="path phi (position S)", ax=ax[1, 1])
    df.plot(x="t", y="total_portfolio_value", title="mismatch", ax=ax[1, 2])
    plt.show()
#Q4ci()


## Question 4d
def Q4d():
    mu = 0.08
    sigma = 0.2
    s0 = 100
    b0 = 1
    r = 0.02
    k =100
    t = 1

    ## gamma call = gamma put
    option = BlackScholesOptionPrice(k,r,sigma)
    gamma = option.gamma(s0,sigma,t)
    print(f"Gamma of the call option: {gamma}")

    ##plotting
    s = np.arange(50,300,1)
    gamma_list = []
    for i in s:
        gamma = option.gamma(i,sigma,t)
        gamma_list.append(gamma)
    ## plot
    plt.figure(f"Q4d")
    plt.plot(s,gamma_list)
    plt.axvline(x=100, color='red')
    plt.xlabel("Stock Price")
    plt.ylabel("Gamma")
    plt.title(f"Gamma of the call option as a function of the stock price")
    plt.legend(["Gamma","Strike Price"])
    plt.show()
#Q4d()