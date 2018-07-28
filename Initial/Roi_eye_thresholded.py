import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt 
import argparse 


face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
black=cv2.imread("black.jpg")
blackedgrey=cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)
gausempt=cv2.adaptiveThreshold(blackedgrey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,2)
gausempt=cv2.resize(gausempt,(100,45))


cap=cv2.VideoCapture(0)
kernel = np.ones((1,1), np.uint8)

def checkdirection(eyes):
	mask = np.zeros(image_array.shape, dtype=np.uint8)
	cv2.circle(mask, max_loc, circle_radius, (255, 255, 255), -1, 8, 0)
	result_array=image_array & mask
	result_array=result_array[max_loc[1]-circle_radius:max_loc[1]+circle_radius]



while True:

	ret,frame=cap.read()
	ret, frame2 =cap.read()
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces=face_cascade.detectMultiScale(gray,1.3,2)
	#face
	for (x,y,w,h) in faces:
        #whole of the face
		cropped=frame[y:y+h,x:x+w]
		frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)

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
			cv2.rectangle(roi_color2,(ex1,ey1),(ex1+ew1,ey1+eh1),(255,0,10),2)

			#thresholding the left eye
			gaus2=cv2.adaptiveThreshold(cropgray2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,2)
			gaus2_copy=gaus2.copy()
			#gaus2_blur = cv2.GaussianBlur(gaus2_copy,(5,5),0 )
			
			#flipping the image so we get a mirror image
			gaus2=cv2.flip(gaus2,1)

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
			eyes[0]=img_dilation


		#Right half of the face 
		roi_color=frame[y:y+h,x:x+int(w/2)]
		roi_gray=gray[y:y+h,x:x+int(w/2)]
		eye_right=eye_cascade.detectMultiScale(roi_gray)

		#right eye
		for (ex,ey,ew,eh) in eye_right :

			#cropping the right eye
			cropped2=cropped[ey+int(eh/2.3):ey+eh-int(eh/4),ex:ex+ew]
			cropgray=cv2.cvtColor(cropped2,cv2.COLOR_BGR2GRAY)
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

			#thresholdig the right eye image
			gaus=cv2.adaptiveThreshold(cropgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,2)
			
            #flipping the image 
			gaus=cv2.flip(gaus,1)

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
        

        #contouring the image to check the eye contours 
		#cn,contours,hierarchy=cv2.findContours(gaus2_blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		#cv2.drawContours(cropped3,contours,-1,(0,255,0),1)	
        
        #showing them beside each other
		numpy_horizontal=np.hstack((eyes[0],eyes[1]))
		cv2.imshow('both eyes',numpy_horizontal)

	cv2.imshow('frame',frame)
	

	if cv2.waitKey(1) & 0xFF==ord('q'):
		break

