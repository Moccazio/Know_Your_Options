# Black–Scholes-Metron

to determine the price of vanilla Europrean options:

1. European options can only be exercised at expiration

2. No dividends are paid during the option's life

3. Market movements cannot be predicted

4. The risk-free rate and volatility are constant

5. Follows a lognormal distribution

For pricing a Call-Option:

$$\textbf{C} = S * N (d_1) - K * e^{-r_k,f *T}*N(d_2)$$

For pricing a Put-Option:

 $$\textbf{P} = K * e^{−r_k,f*T)}N(−d_2)−SN(−d_1)$$



##### where

$$
d_1 = \frac{\ln(\frac{S}{K}) + (r + \frac{stdev^2}{2})t}{s \cdot \sqrt{t}}
$$

$$
d_2 = d_1 - s \cdot \sqrt{t} = \frac{\ln(\frac{S}{K}) + (r - \frac{stdev^2}{2})t}{s \cdot \sqrt{t}}
$$

##### with 

$S$ the spot price of the asset at time t


$T$ the maturity of the option. Time to maturity is defined as T−t


$K$ strike price of the option


$r$ the risk-free interest rate, assumed to be constant between t and T


$\sigma$, volatility of underlying asset, the standard deviation of the asset returns


## Greeks

The greeks are the partial-derivatives of the Black-Scholes equation with respect to each variable. We will create credit spreads so we need the Theta $\Theta$, Delta $\Delta$ and the Gamma $\Gamma$. 

Credit Spread Ratios

$$Risk Ratio = \frac{Net \Theta} {\sqrt{Net \Delta^2 + Net \Gamma^2}}$$

$\Theta$ = the partial-derivative with respect to time until expiration and losing value per day


$\Delta$ = the first partial-derivative with respect to the underlying asset and shows the sensitivity of the option price to a move of the underlying spot price


$\Gamma$ = the 2nd partial-derivative with respect to the underlying asset


$$Cost Ratio = \frac{Net Credit}{Share Cost + Margin Required}$$
