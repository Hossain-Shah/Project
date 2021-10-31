import ffn
#%pylab inline
# download price data from Yahoo! Finance. By default,
# the Adj. Close will be used.
prices = ffn.get('aapl,msft', start='2010-10-30')
# let's compare the relative performance of each stock
# we will rebase here to get a common starting point for both securities
ax = prices.rebase().plot()
# now what do the return distributions look like?
returns = prices.to_returns().dropna()
#ax = returns.hist((10, 5))
# ok now what about some performance metrics?
stats = prices.calc_stats()
stats.display()
# what about the drawdowns?
ax = stats.prices.to_drawdown_series().plot()
