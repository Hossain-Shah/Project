from sklearn.metrics import log_loss
from matplotlib import pyplot
from numpy import array
yhat = [x*0.01 for x in range(0, 101)]
losses_0 = [log_loss([0], [x], labels=[0,1]) for x in yhat]
losses_1 = [log_loss([1], [x], labels=[0,1]) for x in yhat]
pyplot.plot(yhat, losses_0, label='true=0')
pyplot.plot(yhat, losses_1, label='true=1')
pyplot.legend()
pyplot.show()
