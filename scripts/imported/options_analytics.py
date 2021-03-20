import numpy as np
from math import sqrt, pi,log, e 
from enum import Enum
import scipy.stats as stat
from scipy.stats import norm
import time
from pylab import plt
plt.style.use('dark_background')
class BSMerton:
    def __init__(self, args):
        self.Type = int(args[0]) # 1 for a Call, - 1 for a put
        self.S = float(args[1]) 
        self.K = float(args[2]) 
        self.r = float(args[3])
        self.q = float(args[4])
        self.T = float(args[5]) / 365.0 
        self.sigma = float(args[6])
        self.sigmaT = self.sigma * self.T ** 0.5
        self.d1 = (log(self.S / self.K) + 
        (self.r - self.q + 0.5 * (self.sigma ** 2)) 
        * self.T) / self.sigmaT 
        self.d2 = self.d1 - self.sigmaT
        [self.Delta] = self.delta()
    def delta(self):
        dfq = e ** (-self.q * self.T) 
        if self.Type == 1:
            return [dfq * norm.cdf(self.d1)] 
        else:
            return [dfq * (norm.cdf(self.d1) - 1)]
        
    def __init__(self, args):
        self.Type = int(args[0]) # 1 for a Call, - 1 for a put
        self.S = float(args[1]) 
        self.K = float(args[2]) 
        self.r = float(args[3]) 
        self.q = float(args[4]) 
        self.T = float(args[5]) / 365.0
        self.sigma = float(args[6])
        self.sigmaT = self.sigma * self.T ** 0.5
        self.d1 = (log(self.S / self.K) + \
        (self.r - self.q + 0.5 * (self.sigma ** 2)) 
        * self.T) / self.sigmaT 
        self.d2 = self.d1 - self.sigmaT
        [self.Delta] = self.delta()
        [self.Gamma] = self.gamma()
    def gamma(self):
        return [e ** (-self.q * self.T) * norm.pdf(self.d1) / (self.S * self.sigmaT)]    
    
    def __init__ (self, args):
        self.Type = int (args[0]) 
        self.S = float (args [1]) 
        self.K = float (args [2])
        self.r = float (args [3]) 
        self.q = float (args [4]) 
        self.T = float (args [5]) / 365.0
        self.sigma = float (args [6]) 
        self.sigmaT = self.sigma * self.T ** 0.5 
        self.d1 = (log (self.S / self.K) + (self.r - self.q + 0.5 * (self.sigma ** 2)) * self.T) / self.sigmaT 
        self.d2 = self.d1 - self.sigmaT 
        [self.Delta] = self.delta()
        [self.Gamma] = self.gamma()
        [self.Vega] = self.vega ()
    def vega (self):
        return [0.01 * self.S * e ** (- self.q * self.T) * norm.pdf(self.d1) * self.T ** 0.5]