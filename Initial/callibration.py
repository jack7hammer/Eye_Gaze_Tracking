import sigmoid as sig
import numpy as np



def callibration(x,y):
	s=np.amax(x,axis=0)
	x=x/s
	u=np.amax(y,axis=0)
	y=y/u
	np.random.seed(2)
	b=np.random.randn(1)
	syn0=2*np.random.random((2,len(x)))-b
	syn1=2*np.random.random((len(x),2))-b
	for i in range(1,50000):
		l0=x
		l1=sig.sigmoid(np.dot(l0,syn0))
		l2=sig.sigmoid(np.dot(l1,syn1))
		l2err=y-l2
		db=sig.sigmoid(b,deriv=True)
		dl2 = l2err*sig.sigmoid(l2,deriv=True)
		l1err=dl2.dot(syn1.T)
		dl1=l1err*sig.sigmoid(l1,deriv=True)
		syn0+=l0.T.dot(dl1)
		syn1+=l1.T.dot(dl2)
		b+=b*db
	return syn0,syn1,s,b,u
    
      

