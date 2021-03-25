# Know_Your_Options

Black-Scholes-Merton Formula for a Vanilla Call Option:

$c =e^{-qT} S N (d_1) - X e^{-rT} N (d_2)$

$p = X e^{-rT} N (−d_2)−e^{-qT}SN(−d_1)$

With:

$d_1 = \frac{\ln(S/X) + (r  - q \frac{\sigma^2}{2})T}{\sigma  \sqrt{T}}$


$d_2 = d_1 - \sigma \sqrt{T}$

And:

$S$ the spot price of the asset at time t


$T$ the maturity of the option.


$X$ strike price of the option


$r$ the risk-free interest rate, assumed to be constant between t and T


$\sigma$ the  volatility of underlying asset, the standard deviation of the asset returns

$N$ the normal distribution 
