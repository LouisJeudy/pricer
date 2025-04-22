from math import *
from scipy.stats import norm
import yfinance as yf

def get_spot_price(asset):
    ticker = yf.Ticker(asset)
    return ticker.history(period="1d")["Close"].iloc[-1]

def get_calls_put(asset):

    ticker = yf.Ticker(asset)

    spot_price = ticker.history(period="1d")["Close"].iloc[-1]

    # first expiration date
    expiration = ticker.options[0]

    options_chain = ticker.option_chain(expiration)

    # retrieve les calls et puts
    calls = options_chain.calls
    puts = options_chain.puts

    # Affiche les 5 premiers calls
    print("\nExtraits des options Call :")
    print(calls.head())

    # Même chose pour les puts
    print("\nExtraits des options Put :")
    print(puts.head())





def price_black_ascholes_merton(s, k, t, r, sigma, option_type="call"):
    price = 0
    d1 = (log(s / k) + (r + (pow(sigma,2) / 2) * t))/(sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)

    if(option_type == "call"):
        price = s * norm.cdf(d1) - k * exp(-r * t) * norm.cdf(d2)
        delta = norm.cdf(d1)
        theta = (-s * norm.pdf(d1) * sigma / (2 * sqrt(t)) - r * k * exp(-r * t) * norm.cdf(d2)) / 365
        rho = k * t * exp(-r * t) * norm.cdf(d2) / 100
    elif(option_type == "put"):
        price = k * exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        theta = (-s * norm.pdf(d1) * sigma / (2 * sqrt(t)) + r * k * exp(-r * t) * norm.cdf(-d2)) / 365
        rho = -k * t * exp(-r * t) * norm.cdf(-d2) / 100

    else:
        raise ValueError("Option_type should be 'call' or 'put'.")
    
    gamma = norm.pdf(d1) / (s * sigma * sqrt(t))
    vega = s * norm.pdf(d1) * sqrt(t) / 100
    
    return {
        'price': price,
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,
        'rho': rho
    }


s = 100
k = 100
t = 1
r = 0.05
sigma = 0.2

call = price_black_ascholes_merton(s,k,t,r,sigma, "call")
put = price_black_ascholes_merton(s,k,t,r,sigma, "put")

print("--- call ---")
for greek, value in call.items():
    print(f"{greek.capitalize()} : {value:.4f}")

print("--- put ---")
for greek, value in put.items():
    print(f"{greek.capitalize()} : {value:.4f}")

print("--- Spot of AAPL ---")
call_aapl = price_black_ascholes_merton(get_spot_price("TTE"),k,t,r,sigma,"call")
for greek, value in call_aapl.items():
    print(f"{greek.capitalize()} : {value:.4f}")
    
get_calls_put("AAPL")

print(get_spot_price("GLE"))