from scipy.stats import norm
import numpy as np
def black_scholes_option(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return option_price

def european_option_crr(S0, K, T, r, sigma, n=100, option_type='call'):
    # Calcul des paramètres du modèle CRR
    delta_t = T / n
    u = np.exp(sigma * np.sqrt(delta_t))
    d = 1 / u
    p = (np.exp(r * delta_t) - d) / (u - d)
    
    # Initialisation du tableau des prix des actions à la fin de chaque période
    stock_prices = np.zeros((n + 1, n + 1))
    
    # Calcul des prix des actions à la fin de chaque période
    for i in range(n + 1):
        for j in range(i + 1):
            stock_prices[j, i] = S0 * (u ** (i - j)) * (d ** j)
    
    # Calcul des payoffs de l'option à l'échéance
    option_payoffs = np.maximum(0, stock_prices[:, -1] - K) if option_type == 'call' else np.maximum(0, K - stock_prices[:, -1])
    
    # Calcul récursif du prix de l'option
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            option_payoffs[j] = np.exp(-r * delta_t) * (p * option_payoffs[j] + (1 - p) * option_payoffs[j + 1])
    
    return option_payoffs[0]

