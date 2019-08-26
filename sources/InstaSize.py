#!/usr/bin/python
#-*-coding:utf-8 -*
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageOps, ImageCms
import os,pathlib

"""
InstaSize is a program to add borders to your images to keep an Instagram feed with a "paper" effect on your images. 
All portrait images processed by the program have the same size of top / bottom borders and the landscapes have the 
same size of left / right borders to have uniform images. The processed images form squares.

Notes : 

- The directory paths where your source / destination images are stored must not contain spaces. 
Support for Windows paths with spaces is an evolution in progress.

- The application Mac OS X "InstaSize.app" is obligatorily compatible with a version superior to OS X 10.14 Mojave.

- Sometimes, because of a bug, the folder selection buttons do not display text. 
Resize the window with the mouse and the text appears (only with the .app)

Version 1.0

"""

# ------------ Picture Treatment, File Browsing and GUI interactions functions ------------ 

def addBorder(cvsrc,cvdst, cvtitle):

	"""
	Do not return anything. Go through the folder where are the source images without borders. Add borders based on the pixel size of the image and orientation.
	You can change the variable "border_x_y" (borders)
	Default (portrait): 230 px ; (landscape): 200 px
	"""
	# Recovery of paths
	cvsrc+="/"
	cvdst+="/"
	maintitle = cvtitle
	i = 0
	# Browsing images in the source folder
	for picture in os.listdir(cvsrc+"/"):
		if picture.endswith(".jpg"):
			i+=1
			full_path = cvdst+maintitle+str(i)+".jpg"
			img = Image.open(cvsrc+picture)
			width, height = img.size
			# Calculation of the size and orientation of the current image (portrait)
			if height > width:
				orientation = "portrait"
				img = Image.open(cvsrc+picture)
				width, height = img.size
				h_w_border = 0
				h_w_border += height
				h_w_border += (2*230)
				w_w_border = ((h_w_border - width)//2)
				border_x_y = [w_w_border,230]
			# Calculation of the size and orientation of the current image (landscape)
			else:
				orientation = "lanscape"
				h_w_border = 0
				h_w_border += width + (2*200)
				w_w_border = 0
				w_w_border = ((h_w_border - height)//2)
				border_x_y = [200,w_w_border]
				img.close()
			# Definiton of source color space 
			pic = Image.open(cvsrc+picture)
			icc = pic.info.get("icc_profile")
			# Add borders
			ImageOps.expand(pic, border=(border_x_y[0],border_x_y[1],border_x_y[0],border_x_y[1]), fill="white").save(full_path, "JPEG", quality=100, icc_profile=icc)
			pic.close()	
	# Opening a "completed" popup		
	completePopUp()		

def completePopUp():
	"""
	Do not return anything. 
	Opens a window to warn the user that the images have been processed. 
	You can change the text and title of the pop-up.
	"""
	completePopUp = Tk()
	completePopUp.wm_title("Complete")
	label2 = Label(completePopUp, text="The border had successfuly add on your picture with ProPhoto RGB profile")
	label2.pack(side="top", fill="x", pady=10)
	B2 = Button(completePopUp,text="OK", command = completePopUp.destroy)
	B2.pack()
	completePopUp.mainloop()

def browseButtonSrc():
	"""Button to choose the directory where the source images are
	Version 1 of the script does not handle spaces in paths. If the path contains spaces, 
	the function calls failedPopUp () to warn the user to rename their directories.
	"""
	global source_folder_path
	directory = filedialog.askdirectory()
	# Changing the text in the source label
	src_label.config(text=directory)
	source_folder_path = directory

	if " " in source_folder_path:
		failedPopUp()

def browseButtonDst():
	"""Button to choose the directory where the destination images save
	Version 1 of the script does not handle spaces in paths. If the path contains spaces, 
	the function calls failedPopUp () to warn the user to rename their directories.
	"""
	global destination_folder_path
	directory = filedialog.askdirectory()
	# Changing the text in the destination label
	dst_label.config(text=directory)
	destination_folder_path = directory
	if " " in destination_folder_path:
		failedPopUp()

def failedPopUp():
	"""
	Do not return anything. Function called when the user-defined path contains blank spaces
	"""
	failedPopUp = Tk()
	failedPopUp.wm_title("Failed")
	label = Label(failedPopUp, text="Warning. The app don't support blank spaces one filename/directory name ")
	label.pack(side="top", fill="x", pady=10)
	B1 = Button(failedPopUp, text="OK", command = failedPopUp.destroy)
	B1.pack()
	failedPopUp.mainloop()

def submitButton():
	"""
	Do not return anything. 
	Calls the image processing function when the user has entered all the information
	"""
	title_entry = dst_title.get()
	if " " in title_entry:
		failedPopUp()
	else:
		addBorder(source_folder_path,destination_folder_path,title_entry)


# ------------ GUI building ------------ 
gui = Tk()
gui.title("InstaSize v1 - By Guezone")
gui.geometry("800x200")
# Gets the requested values of the height and widht.
windowWidth = gui.winfo_reqwidth()
windowHeight = gui.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(gui.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(gui.winfo_screenheight()/2 - windowHeight/2)
 # Positions the window in the center of the page.
gui.geometry("+{}+{}".format(positionRight, positionDown))
# Button to browse the host to find the source folder, displaying the path in a label
src_button = Button(text="Select source folder", command=browseButtonSrc, width=50)
src_button.pack()
src_label = Label(gui, width=100, justify="left")
src_label.pack()
# Button to browse the host to find the destination folder, displaying the path in a label
dst_button = Button(command=browseButtonDst, width=50)
dst_button.config(text="Select destination folder")
dst_button.pack()
dst_label = Label(gui, width=100, justify="left")
dst_label.pack()
# Enter the file name prefix for images with borders
prefix_label = Label(gui, width=20, justify="left")
prefix_label.pack()
prefix_label.config(text="Enter prefix of output files :")
title = StringVar()
dst_title = Entry(gui, textvariable=title,width=20)
dst_title.pack()
# Submit button
dst_title.bind('<Return>', (lambda event: submitButton()))
submit_button = Button(text="GO !", width=20, command=submitButton)
submit_button.pack()
gui.mainloop()