import pyautogui
import os
import win32api
import time
import callibration as cal
import haar
import time
mouse_length=0
mouse2_length=0
def mouse():
	
	state_left = win32api.GetKeyState(0x01)
	global mosue_length
	global mouse2_length

	i=0
	mouse=[]
	mouse2=[]
	while i<45:
		a = win32api.GetKeyState(0x01)
		if a != state_left:
			state_left = a
			if a < 0:
				mouse.append(pyautogui.position())
				mouse2.append(pyautogui.position())
				mouse_length=len(mouse)
				mouse2_length=len(mouse2)
				time.sleep(0.0001)
				if(mouse_length>haar.eye_coordinates_left_length):					
					mouse.pop()
				if(mouse2_length>haar.eye_coordinates_right_length):
					mouse2.pop()


				i+=1
	return mouse,mouse2







