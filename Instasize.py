#!/usr/bin/python
#-*-coding:utf-8 -*
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageOps, ImageCms
import os,pathlib

srcdir = ""
dstdir = ""
maintitle = ""
#colorspace = ""



def AddBorder(cvsrc,cvdst, cvtitle):
	cvsrc+="/"
	cvdst+="/"
	maintitle = cvtitle
	
	i = 0
	for picture in os.listdir(cvsrc+"/"):
		if picture.endswith(".jpg"):
			i+=1





			full_path = cvdst+maintitle+str(i)+".jpg"



			img = Image.open(cvsrc+picture)
			width, height = img.size
		
			# Portrait pictures
			if height > width:
				orientation = "portrait"
				img = Image.open(cvsrc+picture)
				width, height = img.size

				h_w_border = 0
				h_w_border += height
				h_w_border += (2*230)
		

				w_w_border = ((h_w_border - width)//2)
				border_x_y = [int(w_w_border),230]

			# Landscape pictures
			else:
				orientation = "lanscape"

				h_w_border = 0
				h_w_border += width 
				h_w_border += (2*200)

				h_w_border = ((h_w_border - width)//2)
				border_x_y = [200,w_w_border]
				img.close()





			pic = Image.open(cvsrc+picture)
			icc = pic.info.get("icc_profile")
			ImageOps.expand(pic, border=(border_x_y[0],border_x_y[1],border_x_y[0],border_x_y[1]), fill="white").save(full_path, "JPEG", quality=100, icc_profile=icc)

		
	popUp2()		

def popUp2():
	popup2 = Tk()
	popup2.wm_title("Complete")
	label2 = Label(popup2, text="The border had successfuly add on your picture with ProPhoto RGB profile")
	label2.pack(side="top", fill="x", pady=10)
	B2 = Button(popup2,text="OK", command = popup2.destroy)
	B2.pack()
	popup2.mainloop()


	
def browseButtonSrc():
# Allow user to select a directory and store it in global var
# called source_folder_path
	global source_folder_path
	directory = filedialog.askdirectory()
	pathlabelSRC.config(text=directory)
	source_folder_path = directory

	if " " in source_folder_path:
		popUp()
	
# def getRgb(event):
# 	colorspace = ""
# 	colorspace += str((rgb.curselection(ACTIVE)))


def browseButtonDst():
# Allow user to select a directory and store it in global var
# called source_folder_path
	global destination_folder_path
	directory = filedialog.askdirectory()
	pathlabelDST.config(text=directory)
	destination_folder_path = directory

	if " " in destination_folder_path:
		popUp()

	
def popUp():
	popup = Tk()
	popup.wm_title("Failed")
	label = Label(popup, text="Warning. The app don't support blank spaces one filename/directory name ")
	label.pack(side="top", fill="x", pady=10)
	B1 = Button(popup, text="OK", command = popup.destroy)
	B1.pack()
	popup.mainloop()


def goButton():

	title_entry = titleDST.get()
	if " " in title_entry:
		popUp()
	else:
		AddBorder(source_folder_path,destination_folder_path,title_entry)





root = Tk()
root.title("InstaSize v1 - By Guezone")
root.geometry("800x2000")
# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

buttonSRC = Button(text="Select source folder", command=browseButtonSrc, width=50)
buttonSRC.pack()

pathlabelSRC = Label(root, width=50, justify="left")
pathlabelSRC.pack()


buttonDST = Button(command=browseButtonDst, width=50)
buttonDST.config(text="Select destination folder")
buttonDST.pack()


pathlabelDST = Label(root, width=50, justify="left")
pathlabelDST.pack()


# colorprofile = Label(root, width=50, justify="left")
# colorprofile.pack()
# colorprofile.config(text="Choose your RGB profile : ")

# rgb = Listbox(root)
# rgb.insert(0, 'AdobeRGB1998')
# rgb.insert(1, 'ProPhoto')
# rgb.insert(2, 'sRGB')
# rgb.pack()
# rgb.bind('<<ListboxSelect>>',getRgb)





titlelabel = Label(root, width=50, justify="left")
titlelabel.pack()
titlelabel.config(text="Enter prefix of output files :")

title = StringVar()
titleDST = Entry(root, textvariable=title,width=50)
titleDST.pack()
titleDST.bind('<Return>', (lambda event: goButton()))

buttonTIT = Button(text="GO !", width=50, command=goButton)
buttonTIT.pack()


root.mainloop()
