import threading 
from queue import Queue
import time 
import mouse as mou
import interface as inte
global m
import haar

def firstjob(worker):
	global m
	m=mou.mouse()
	haar.callibration=False
	print("\nLeft eye coordinates \n", haar.eye_coordinates_left)
	
	print("\nright eye coordinates\n", haar.eye_coordinates_right)
	print("\nscreen coordinates\n", m)


	
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


