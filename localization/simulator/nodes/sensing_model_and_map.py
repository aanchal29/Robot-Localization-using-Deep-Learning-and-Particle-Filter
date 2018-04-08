import math

# definition of normal curve
def gauss (x, mu, sigma):
    exp= 0 - (((float(x)-float(mu))** 2) / (2 * float(sigma) * float(sigma)))
    return (1/(float(sigma) * math.sqrt(2*math.pi))) * (math.e ** exp)

# this experimentally approximates door sensor performance
def door(mu, x):
    sigma= .75
    peak= gauss(0, 0, sigma)   
    return 0.8 * gauss(x, mu, sigma)/peak

# doors are centered at 11m, 18.5m, and 41m
def p_door(x):
    return 0.1 + door(11, x) + door(18.5, x) + door(41, x)

def p_wall(x):
    return 1.0 - p_door(x)
