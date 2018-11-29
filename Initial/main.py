import threading 
from queue import Queue
import time 
import mouse as mou
import interface as inte
global m
import haar
import callibration as cal


def firstjob(worker):
	global m
	m,n=mou.mouse()
	fp=open("data.txt","w")
	fp.write('{0}\n {1}\n {2}\n {3}\n'.format(haar.eye_coordinates_left, m , haar.eye_coordinates_right,n))
	fp.close()
	print("\n\n\t\t\t         ..... TRAINING ....\n\n\n")
	haar.left_syn0,haar.left_syn1,haar.left_s,haar.left_b,haar.left_u=cal.callibration(haar.eye_coordinates_left,m)
	haar.right_syn0,haar.right_syn1,haar.right_s,haar.right_b,haar.right_u=cal.callibration(haar.eye_coordinates_right,n)
	print("Training - Done!")
	haar.callibration=False

	


	
def secondjob(worker):	
	inte.interface()

def  thirdjob(worker):
	haar.eyes()
	
def threader():
	while  True:

		worker=q.get()
		firstjob(worker)
		q.task_done()	
def threader2():
	while True:
		worker2=q.get()
		secondjob(worker2)
		q.task_done()
def threader3():
	while True:
		worker3=q.get()
		thirdjob(worker3)
		q.task_done()


q=Queue()
t3=threading.Thread(target=threader3)
t3.daemon=True
t3.start()
time.sleep(5)
t2=threading.Thread(target= threader2)
t2.daemon=True
t2.start()
t1= threading.Thread(target = threader)
t1.daemon=True
t1.start()







for worker in range(3):
	q.put(worker)
q.join()

global m


