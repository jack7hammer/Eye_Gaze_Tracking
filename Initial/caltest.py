import callibration as cal
import numpy as np
import sigmoid as sig

def calltest(syn0,syn1,s,b,u,unknown,message):

	unknown=unknown/s
	layer1=sig.sigmoid(np.dot(unknown,syn0))-b
	layer2=sig.sigmoid(np.dot(layer1,syn1))-b
	print(message,layer2*u)
	



