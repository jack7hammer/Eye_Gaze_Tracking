import numpy as np
def sigmoid(x, deriv=False):
	if deriv== True:
		return x*(1-x)
	return 1/(1+np.exp(-x))


