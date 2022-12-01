## group 5

## modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from mpl_toolkits.mplot3d import Axes3D


class StochasticProcess:
    """Base class for simulating stochastic processes.

    Warning: This class should not be used directly. Use derived classes instead.
    """

    def __init__(self, name, time_grid, paths):
        self.name = name
        self.time_grid = time_grid
        self.paths = paths
        self.params = None

    def plot(self, num_paths=5):
        """Plots (minimum of number of available sample paths and num_paths) sample paths.

        Args:
            num_paths (int): number of sample paths to be plotted. Defaults to 5.
        """

        num_paths = min(self.paths.shape[0], num_paths)
        paths = self.paths[:num_paths, :].T
        title = f"{num_paths} simulated sample paths from {self.name}"
        if self.params is not None:
            title += f" with parameters: {[(k, v) for k, v in self.params.items()]}"
        pd.DataFrame(
            paths,
            columns=[f"path {j}" for j in range(1, 1 + num_paths)],
            index=self.time_grid,
        ).plot(kind="line", title=title, figsize=(25, 7))

    def avg_and_var_over_simulations(self):
        """Calculates, for each point on time-grid, the mean and variance over sample paths."""

        if not self.paths.shape[0] > 0:
            raise ValueError("Requires minimum of two paths.")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 7))
        aux = np.mean(self.paths, axis=0)
        avg_df = pd.DataFrame(aux, columns=["Average over paths"], index=self.time_grid)
        avg_df.plot(kind="line", title="Average over sample paths", ax=ax1)
        aux = np.var(self.paths, axis=0)
        var_df = pd.DataFrame(
            aux, columns=["Var over sample paths"], index=self.time_grid
        )
        var_df.plot(kind="line", title="Var over sample paths", ax=ax2)
        return avg_df, var_df


class BrownianMotionWithDrift(StochasticProcess):
    """Class to simulate paths of a Brownian motion with drift, i.e. X_t = ct + W_t"""

    def __init__(self, drift, sigma, n, T, time_step, seed=None):

        if T < time_step:
            raise ValueError("Maturity T should be larger than time step.")
        if sigma < 0:
            raise ValueError("sigma should be strictly positive.")
        self.n = n
        self.T = T
        self.time_grid, self.time_step = np.linspace(
            0, self.T, num=1 + int(T / time_step), endpoint=True, retstep=True
        )  # note that time_step is adapted (if needed) in order to get equally-spaced grid
        if seed is not None:
            np.random.seed(seed)
        aux = np.random.normal(loc=0.0, scale=1.0, size=(self.n, len(self.time_grid)-1))
        aux = np.concatenate([np.zeros((self.n, 1)), aux], axis=1)
        self.paths = (
            np.cumsum(sigma * np.sqrt(time_step) * aux, axis=1) + drift * self.time_grid
        )
        super().__init__("Brownian Motion with drift", self.time_grid, self.paths)
        self.params = {"drift c": drift, "sigma": sigma}


class BrownianMotion(BrownianMotionWithDrift):
    """Class to simulate paths of a Brownian motion"""

    def __init__(self, sigma, n, T, time_step, seed=None):

        super().__init__(0, sigma, n, T, time_step, seed)
        self.name = "Brownian Motion"
        self.params = {"sigma": sigma}


class GeometricBrownianMotion(BrownianMotionWithDrift):
    """Class to simulate paths of a Geometric Brownian motion, i.e. X_t=X_0\exp((mu-0.5sigma^2)t+sigma*W_t)"""

    def __init__(self, starting_value, mu, sigma, n, T, time_step, seed=None):

        super().__init__(mu - 0.5 * sigma ** 2, sigma, n, T, time_step, seed)
        self.paths = starting_value * np.exp(self.paths)
        self.name = "Geometric Brownian Motion"
        self.params = {"starting_value": starting_value, "mu": mu, "sigma": sigma}

class ItoDiffusionEuler(BrownianMotion):
    """Class to simulate approximations to solution of SDE dX_t = a(t, X_t) dt + b(t, X_t) dW_t,
    X_0=x_0 and where W is a standard Brownian motion."""
        
    def __init__(
        self,
        starting_value,
        drift_function,
        volatility_function,
        n,
        T,
        time_step,
        seed=None,
    ):

        super().__init__(1, n, T, time_step, seed)
        self.name = "Euler approximation to Ito diffusion dX_t=mu(X_t)+sigma(X_t)dW_t"
        self.dW = (
            self.paths[:, 1:] - self.paths[:, :-1]
        )  # increments standard Brownian motion
        self.paths[:, 0] = starting_value
        for j in range(1, self.paths.shape[1]):
            previous = self.paths[:, j - 1]
            self.paths[:, j] = (
                previous
                + drift_function(self.time_grid[j - 1], previous) * self.time_step
                + volatility_function(self.time_grid[j - 1], previous)
                * self.dW[:, j - 1]
            )
        self.params = {"drift": drift_function, "volatility": volatility_function}

class BlackScholesOptionPrice():
    """Class for Black-Scholes price of European put and call options."""

    def __init__(self, strike: float, r: float, sigma: float):
        
        self.r = r
        self.sigma = sigma
        self.strike = strike

    def _d1_and_d2(self, current_stock_price, time_to_maturity):
        """Calculates auxiliary d_1 and d_2 which enter the N(0, 1) cdf in the pricing formulas"""
        
        d1 = (np.log(current_stock_price / self.strike) + (self.r + 0.5 * self.sigma ** 2) * time_to_maturity) / (self.sigma * np.sqrt(time_to_maturity))
        d2 = d1 - self.sigma * np.sqrt(time_to_maturity)
        return d1, d2

    def price_put(self, current_stock_price, time_to_maturity):
        """Calculates price of European put option"""

        d1, d2 = self._d1_and_d2(current_stock_price, time_to_maturity)
        return np.exp(-self.r * time_to_maturity) * self.strike * norm.cdf(-d2) - current_stock_price * norm.cdf(-d1)
    
    def delta_put(self, current_stock_price, time_to_maturity):
        """Calculates delta of European put option."""
        
        d1, _ = self._d1_and_d2(current_stock_price, time_to_maturity)
        return - norm.cdf(- d1)
                
    def price_call(self, current_stock_price, time_to_maturity):
        """Calculates price of European call option"""

        d1, d2 = self._d1_and_d2(current_stock_price, time_to_maturity)
        return current_stock_price * norm.cdf(d1) - np.exp(-self.r * time_to_maturity) * self.strike *  norm.cdf(d2)
    
    def delta_call(self, current_stock_price, time_to_maturity):
        """Calculates delta of European call option."""
        
        d1, _ = self._d1_and_d2(current_stock_price, time_to_maturity)
        return norm.cdf(d1)
    
    def gamma(self,current_stock_price,sigma,time_to_maturity):
        """Calculates gamma of European option."""
        d1, _ = self._d1_and_d2(current_stock_price, time_to_maturity)
        return (1/(current_stock_price*sigma*np.sqrt(time_to_maturity)))*norm.cdf(d1)
    
    def _vega(self, current_stock_price, time_to_maturity):
        """Computes vega."""
        
        d1, _ = self._d1_and_d2(current_stock_price, time_to_maturity)
        return current_stock_price * norm.pdf(d1) * np.sqrt(time_to_maturity)
    
    def vega_call(self, current_stock_price, time_to_maturity):
        return self._vega(current_stock_price, time_to_maturity)

    def vega_put(self, current_stock_price, time_to_maturity):
        return self._vega(current_stock_price, time_to_maturity)  

class NumericalProxyPDE:
    """Class implementing the algorithm that has been described above."""

    def __init__(
        self,
        Smax: float,
        dS: float,
        K: float,
        dT: float,
        T: float,
        r: float,
        sigma: float,
    ):

        self.M = int(np.ceil(Smax / dS))  # number of points in grid for stockprice
        self.ds = Smax / self.M  # mesh in grid for stockprice
        self.N = int(np.ceil(T / dT))  # number of points in grid for time
        self.dt = T / self.N  # mesh in grid for time
        self.t = np.linspace(0, T, self.N + 1)
        self.S = np.linspace(0, Smax, self.M + 1)
        J = np.arange(1, self.M - 1 + 1)
        self.a = 0.5 * r * J * self.dt - 0.5 * sigma ** 2 * J ** 2 * self.dt
        b = 1 + sigma ** 2 * self.dt * J ** 2 + r * self.dt
        self.c = -0.5 * r * self.dt * J - 0.5 * sigma ** 2 * self.dt * J ** 2
        self.A = diags([self.a[1:], b, self.c[:-1]], offsets=[-1, 0, 1])
        self.G = np.zeros((self.N + 1, self.M + 1))  # time x stock price
        self.Smax = Smax

    def solve_pde(self, boundary_equation_maturity, boundary_equation_smax):

        # set boundary conditions (for payoff at maturity):
        self.G[self.N, :] = boundary_equation_maturity(
            self.S
        )  # boundary at t=T, i.e. pay-off
        self.G[:, self.M] = boundary_equation_smax(
            self.t
        )  # boundary a t  and S=Smax, note that this approximation only makes sense if Smax is large enough!
        self.G[:, 0] = boundary_equation_maturity(0)  # if S = 0 then S_t is constant
        # set up difference equation

        # solve V recursively
        for i in range(self.N, 0, -1):
            y = np.ravel(self.G[i, 1 : self.M])
            y[0] = y[0] - self.a[0] * boundary_equation_maturity(0)
            y[-1] = y[-1] - self.c[-1] * boundary_equation_smax(self.Smax)

            self.G[i - 1, 1 : self.M] = np.transpose(spsolve(self.A, y))

class SolvePDEBoundaryNumerically(NumericalProxyPDE):

    def __init__(
        self,
        Smax: float,
        dS: float,
        K: float,
        dT: float,
        T: float,
        r: float,
        sigma: float,
        boundary_equation_maturity,
        boundary_equation_smax,
    ):

        super().__init__(Smax, dS, K, dT, T, r, sigma)
        self.solve_pde(boundary_equation_maturity, boundary_equation_smax)

    def plot_price(self):

        f, ax = plt.subplots(figsize=(25, 7))
        ax.plot(self.S, self.G[0, :])
        ax.set_title("Price option at t=0 as function of $s_0$")
        ax.set_xlabel("s_0")
        ax.set_ylabel("price option")
        return ax

    def price_specific_point(self, t, s):
        """Determines price option at time t for stock price S_t=s"""

        nearest_idx_stock_price = np.where(abs(self.S - s) == abs(self.S - s).min())[0][
            0
        ]  # find index of point in stock price grid closest to S_0
        nearest_idx_time = np.where(abs(self.t - t) == abs(self.t - t).min())[0][
            0
        ]  # find index of point in stock price grid closest to S_0
        stock_price = self.S[
            nearest_idx_stock_price
        ]  # If you directly want the element of array (array) nearest to the given number (num)
        time = self.t[nearest_idx_time]
        """
        
        print(
            f"The closest point to specified s on the grid is {stock_price} and the closest point to specified t is {time}"
        )"""
        price = self.G[nearest_idx_time, nearest_idx_stock_price]
        """
        
        print(
            f"The (approximation to the) price of the option at t={time}, S_t={stock_price} is {price}"
        )"""
        return price

def approximate_vega_call_bump_reprice_osfd_noncommon(num_replications, T, sigma, r, K,S_0, h):

    def aux(T, r, sigma):
        S_T =  S_0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma *  np.sqrt(T) * norm.rvs(size=num_replications))
        option_price_prox = np.exp(-r * T) * np.mean(np.maximum(S_T - K, 0))
        return option_price_prox
    return (aux(T, r, sigma + h) - aux(T, r, sigma)) / h

def writing_put_option_delta_hedge_discrete_time(K: float, T: float, S_0: float, mu: float, sigma: float,
                                                 B_0: float, r: float, num_time_steps_per_unit_of_time: int,
                                                num_puts: int
                                                 ):

    num_time_steps_total = int(T * num_time_steps_per_unit_of_time)
    time_delta = T / num_time_steps_total
    # intitialize variables:
    phi = np.zeros(num_time_steps_total + 1)
    psi = np.zeros(num_time_steps_total + 1)
    phi[-1] = np.nan
    psi[-1] = np.nan
    price_puts = np.zeros(num_time_steps_total + 1)
    S = np.zeros(num_time_steps_total + 1)
    S[0] = S_0
    B = np.zeros(num_time_steps_total + 1)
    B[0] = B_0
    total_portfolio_value = np.zeros(num_time_steps_total + 1)
    put = BlackScholesOptionPrice(K, r, sigma)
    time = np.linspace(0, T, num_time_steps_total + 1)
    # determine initial positions:
    put_price_initial = put.price_put(current_stock_price=S_0, time_to_maturity=T)
    price_puts[0] = num_puts * put_price_initial
    phi[0] = - num_puts * put.delta_put(current_stock_price=S_0, time_to_maturity=T) # make total portfolio delta-neutral
    psi[0] = - (price_puts[0] + phi[0] * S[0]) / B[0]
    total_portfolio_value[0] = price_puts[0] + phi[0] * S[0] + psi[0] * B[0] # 0 by construction
    # iterate over discrete-time grid:
    for k in range(1, num_time_steps_total + 1):
        # new asset prices:
        B[k] = B[k - 1] * np.exp(r * time_delta)
        S[k] = S[k - 1] * np.exp((mu - 0.5 * sigma ** 2) * time_delta + sigma * np.sqrt(time_delta) * norm.rvs())
        # current value of (S,B) portfolio from previous point-in-time (below we will rebalance):
        value = phi[k - 1] * S[k] + psi[k - 1] * B[k]
        # new value puts:
        if time[k] == T:
            price_puts[k] =  num_puts * np.maximum(K - S[k], 0)
            total_portfolio_value[k] = price_puts[k] + value
            break 
        price_puts[k] = num_puts * put.price_put(current_stock_price=S[k], time_to_maturity=T - time[k])
        # determine new position S for next interval (such that combination of (S, B)-portfolio and 
        # puts is delta-neutral):
        phi[k] =  - num_puts * put.delta_put(current_stock_price=S[k], time_to_maturity=T - time[k])
        # determine new position B, such that there is no net cashflow in (S, B)-portfolio:
        psi[k] = (value - phi[k] * S[k]) / B[k]
        # mismatch between discrete-time delta-neutral, self-financing portfolio and price puts:
        total_portfolio_value[k] = price_puts[k] + phi[k] * S[k] + psi[k] * B[k]
    return time, S, B, phi, psi, price_puts, total_portfolio_value
    