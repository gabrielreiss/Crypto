from scipy.stats import norm

def z(numero):
    media=720
    sd = 30
    z = (numero-media)/sd
    return z

norm.cdf(z(750)) - norm.cdf(z(650)) 
norm.cdf(-z(800))
norm.cdf(z(700))

norm.cdf(1.96)
norm.cdf(-2.15)
norm.cdf(-0.78)
norm.cdf(-0.59)