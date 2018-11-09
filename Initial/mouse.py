import pyautogui
import os
import win32api
import time
import callibration as cal


def mouse():

	state_left = win32api.GetKeyState(0x01)

	i=0
	mouse=[]
	while i<45:
		a = win32api.GetKeyState(0x01)
		if a != state_left:
			state_left = a
			if a < 0:
				mouse.append(pyautogui.position())
				i+=1
	return mouse







