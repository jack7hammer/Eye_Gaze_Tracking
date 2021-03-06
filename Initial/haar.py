import numpy as np
import os
import cv2
import imutils
import matplotlib.pyplot as plt 
import argparse 
import sigmoid as sig
import win32api
import pyautogui
import time
import caltest as callt
import winsound

#import mouse
left_syn0=[[]]
left_syn1=[[]]
left_b=0
left_s=[]
left_u=[]
right_syn0=[[]]
right_syn1=[[]]
right_b=0
right_s=[]
right_u=[]


s=0
f=0
#Pre trained calssifiers for face and eyes
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')

#for a blank image as initialization 
black=cv2.imread("black.jpg")
blackedgrey=cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)


gausempt=cv2.adaptiveThreshold(blackedgrey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,25)
gausempt=cv2.resize(gausempt,(100,45))


cap=cv2.VideoCapture(0)
kernel = np.ones((5,5),np.uint8)

eye_coordinates_left=[]
eye_coordinates_right=[]

callibration=True
eye_coordinates_left_length=0
eye_coordinates_right_length=0

global state_left
state_left = win32api.GetKeyState(0x01)

def centroid(cnt,txt):
	m=cv2.moments(cnt)

	#centroid x coordinate
	cx=int(m['m10']/m['m00'])

	#centroid y coordinate
	cy=int(m['m01']/m['m00'])
	
	return cx,cy

	
def DisplayWarning(text):
	print("\n\n\n\n \t\t\t WARNING",text)
	winsound.Beep(2500,500)



def eyes():

	global left_syn0
	global right_syn0
	global left_syn1
	global right_syn1
	global left_b
	global right_b
	global left_s
	global right_s 
	global left_u
	global right_u

	while True:

		ret,frame=cap.read()
		ret, frame2 =cap.read()
		gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
		gray=clahe.apply(gray)

		faces=face_cascade.detectMultiScale(gray,1.3,2)
		#face
		global f
		if len(faces)==0 and f==0:
			f=time.time()
		if len(faces)==0:
			y=time.time()-f
			if y>2 :
				DisplayWarning("FACE NOT FOUND")
		if len(faces)!=0:
			f=0
			


		for (x,y,w,h) in faces:

	        #whole of the face
			cropped=frame[y:y+h,x:x+w]
			frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),1)

			#initializing the list with blank images
			eyes=[gausempt,gausempt]

	        #left half of the face
			roi_color2=frame[y:y+h,x+int(w/2):x+w]
			roi_gray2=gray[y:y+h,x+int(w/2):x+w]
			eye_left=eye_cascade.detectMultiScale(roi_gray2)
	         
	        #left eye
			for (ex1,ey1,ew1,eh1) in eye_left :

				#cropping the left eye
				cropped3=cropped[ey1+int(eh1/2.3):ey1+eh1-int(eh1/4),ex1+int(w/2):ex1+int(w/2)+ew1]
				cropgray2=cv2.cvtColor(cropped3,cv2.COLOR_BGR2GRAY)
				
				cv2.rectangle(roi_color2,(ex1,ey1),(ex1+ew1,ey1+eh1),(255,255,255),1)

				#thresholding the left eye
				gaus2=cv2.adaptiveThreshold(cropgray2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,10)
				gaus2_copy=gaus2.copy()
				gaus2_inv=cv2.bitwise_not(gaus2_copy)
				gaus2_closing=cv2.morphologyEx(gaus2_inv,cv2.MORPH_CLOSE,kernel)

				gaus2_opening = cv2.morphologyEx(gaus2_closing, cv2.MORPH_OPEN, kernel)


				#gaus2_blur = cv2.GaussianBlur(gaus2_inv,(5,5),0 )
				#flipping the image so we get a mirror image
				gaus2=cv2.flip(gaus2_opening,1)
				

				#resizing the image to a fixed dimensions
				gausl=cv2.resize(gaus2,(100,45))
				#cv2.imshow("threshold left",gausl)
				img_dilation = cv2.dilate(gausl, kernel, iterations=1)

				#finding the dimensions of the thresholded image
				height=np.size(gausl,0)
				width=np.size(gausl,1)

				#checking if the threshold exists or not
				#if height==100 and width ==60:
	                
	                #if it does then add it to the eyes list
				eyes[0]=gausl


			#Right half of the face 
			roi_color=frame[y:y+h,x:x+int(w/2)]
			roi_gray=gray[y:y+h,x:x+int(w/2)]
			eye_right=eye_cascade.detectMultiScale(roi_gray)

			#right eye
			for (ex,ey,ew,eh) in eye_right :

				#cropping the right eye
				cropped2=cropped[ey+int(eh/2.3):ey+eh-int(eh/4),ex+int(ex/5):ex+ew-int(ex/5)]
				cropgray=cv2.cvtColor(cropped2,cv2.COLOR_BGR2GRAY)
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),1)


				#thresholdig the right eye image
				gaus=cv2.adaptiveThreshold(cropgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,10)
				gaus_copy=gaus.copy()
				gaus_inv=cv2.bitwise_not(gaus_copy)

				gaus_closing=cv2.morphologyEx(gaus_inv,cv2.MORPH_CLOSE,kernel)

				gaus_opening = cv2.morphologyEx(gaus_closing, cv2.MORPH_OPEN, kernel)


				#gaus_blur=cv2.GaussianBlur(gaus_inv,(5,5),0)

	            #flipping the image 
				gaus=cv2.flip(gaus_opening,1)

				#resizing the image to get a fixed dimension
				gausr=cv2.resize(gaus,(100,45))
				#cv2.imshow("threshold_right",gausr)

				#finding the dimensions of the thresholded image
				height=np.size(gausr,0)
				width=np.size(gausr,1)

				#checking if the threshold exists or not 
				#if height==100 and width ==60:

					#if it exits then add it to the eyes list in 1 index
				eyes[1]=gausr

	        #contouring the image to check the left eye contours 
			cn,contours,hierarchy=cv2.findContours(gaus2_opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
			cv2.drawContours(cropped3,contours,-1,(0,255,0),1)
			#a,b=centroid(contours[0],"left eye")
			#contoursv2.drawContours(cropped3,(a,b),20,(255,255,0),2)


			cn2,contours2,hierarchy2=cv2.findContours(gaus_opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
			cv2.drawContours(cropped2,contours2,-1,(0,255,0),1)
			global s

			if (s==0 and len(contours2)==0 and len(contours)==0 and f==0) or(s==0 and len(contours)==0 and ew==0 and f==0) or (s==0 and len(contours2)==0 and ew1==0 and f==0) or (ew==0 and ew1==0) :
				s=time.time()
			if (len(contours)==0 and len(contours2)==0 and f==0) or(f==0 and len(contours)==0 and ew==0) or (f==0 and len(contours2)==0 and ew1==0) or (ew==0 and ew1==0):
				x=time.time()-s
				if x > 2:
					DisplayWarning("EYES NOT DETECTED")
				
			if len(contours)!=0 or len(contours2)!=0:
				s=0
			
			if len(contours)>0:
				cnt=contours[0]
				x,y=centroid(cnt,"left eye")

			if len(contours2)>0:
				cnt=contours2[0]
				x1,y1=centroid(cnt,"right eye")
	        
	        #showing them beside each other
			numpy_horizontal=np.hstack((eyes[0],eyes[1]))
			cv2.imshow('both eyes',numpy_horizontal)

		if callibration == True:
			global eye_coordinates_left_length
			global eye_coordinates_right_length
			global state_left

			a= win32api.GetKeyState(0x01)
			if a != state_left:
				state_left = a
				if a < 0:
					if(x or y):
						eye_coordinates_left.append([x,y])
						eye_coordinates_left_length= len(eye_coordinates_left)
					if(x1 or y1):
						eye_coordinates_right.append([x1,y1])
						eye_coordinates_right_length = len(eye_coordinates_right)
			#print(eye_coordinates_left)
			#print(eye_coordinates_right)

		if callibration==False:
			if([x,y]):
				callt.calltest(left_syn0,left_syn1,left_s,left_b,left_u,([x,y]),"left")
			if([x1,y1]):
				callt.calltest(right_syn0,right_syn1,right_s,right_b,right_u,([x1,y1]),"right")

		cv2.imshow('frame',frame)
		

		if cv2.waitKey(1) & 0xFF==ord('q'):
			break

eyes()

