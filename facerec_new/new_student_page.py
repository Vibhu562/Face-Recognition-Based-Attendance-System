import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
from new_student_support import *
from functools import partial


filename= ""
fname = ""
lname = ""
adm = ""
sn = ""
cs =""
pno =""
photo = ""


root = tk.Tk()
root.geometry("620x440")
root.title("Student details")
root['background']='#add8e6'

def fileDialog():
	global filename
	filename = filedialog.askopenfilename(initialdir = "/", title = "Choose a photo", filetype= (("All Files","*.*"),("jpeg","*.jpeg"),("jpg","*.jpg")))
	flocation.configure(text = filename)

def open_img():
	global photo
	fileDialog() 
	img = Image.open(filename) 
	img = img.resize((100, 120), Image.ANTIALIAS) 
	img = ImageTk.PhotoImage(img) 

	#image
	photo= tk.Label(subhead,image=img)
	photo.place(x= 0, y=0, height= 120, width=100)
	photo.image = img 
	
def submit():
	global fname
	global lname
	global adm
	global sn
	global cs
	global pno
	lname = known_lname.get()
	fname = known_fname.get()
	sn = session.get()
	cs = std.get()
	pno = phone.get()
	adm = adm_no.get()
	stData_local(filename,fname,lname,adm,cs)
	stData_database(adm,fname,lname,sn,cs,pno)


	confirmation.insert(tk.END,"Student record added")

def clear():
	known_fname.delete(0,"end")
	known_lname.delete(0,"end")
	session.delete(0,"end")
	std.delete(0,"end")
	phone.delete(0,"end")
	adm_no.delete(0,"end")
	flocation.configure(text = "")
	photo.destroy()

def back():
	root.destroy()

#head label
head = tk.Label(root)
head.place(x=20, y=20, width=620-20-20, height=120+2)
head['background']='#add8e6'

#heading
w = tk.Label(head, text="STUDENT DETAILS",font=("Helvetica",22,"underline","bold"), fg="black")
w.place(x=40,y=20, width=270,height=80)
w['background']='#add8e6'


#subhead
subhead= tk.Label(head,relief=tk.RIDGE, text= "image preview", fg="black")
subhead.place(x= 420, y=0, height= 120, width=100)


#mid label
mid = tk.Label(root)
mid.place(x=20, y=60+40+40+20, width=570, height=195)
mid['background']='#add8e6'

#adm no
w = tk.Label(mid,relief=tk.RIDGE, text="Admission no",  fg="black")
w.place(x = 0, y = 0 , width=120, height=25)
adm_no = tk.Entry(mid)
adm_no.place(x=130,y=0, width=140,height=25)

#first name
w = tk.Label(mid,relief=tk.RIDGE, text="First Name",  fg="black")
w.place(x = 0, y = 40 , width=120, height=25)
known_fname = tk.Entry(mid)
known_fname.place(x=130,y=40, width=140,height=25)

#session
w = tk.Label(mid,relief=tk.RIDGE, text="Session",  fg="black")
w.place(x = 300, y = 0, width=120, height=25)
session = tk.Entry(mid)
session.place(x=430,y=0, width=140,height=25)

#last name
w = tk.Label(mid,relief=tk.RIDGE, text="Last Name",  fg="black")
w.place(x = 300, y = 40 , width=120, height=25)
known_lname = tk.Entry(mid)
known_lname.place(x=430,y=40, width=140,height=25)

#class
w = tk.Label(mid,relief=tk.RIDGE, text="Class",  fg="black")
w.place(x = 0, y = 40+40 , width=120, height=25)
std = tk.Entry(mid)
std.place(x=130,y=40+40, width=140,height=25)

#phone no
w = tk.Label(mid,relief=tk.RIDGE, text="Phone No",  fg="black")
w.place(x = 300, y = 40+40 , width=120, height=25)
phone = tk.Entry(mid)
phone.place(x=430,y=40+40, width=140,height=25)

#photo
plabel = tk.Label(mid)
plabel.place(x = 0, y = 40+40+50 , height=63, width=270)
plabel['background']='#add8e6'

ph= tk.Label(plabel, relief=tk.RIDGE, text="Student Photo", fg= "black")
ph.place(x=0, y=0, width=130, height=25)

browse = tk.Button(plabel, width=10, text="Browse", fg="black", bg="#B6BABA", command = open_img)
browse.place(x=130, y=0, width=140, height=25)

flocation=tk.Label(plabel, relief=tk.RIDGE, fg= "black", text= "")
flocation.place(x=0, y=40, width=268)


#confirmation window
confirmation = tk.Text(mid, fg="black",font=(12))
confirmation.place(x=300,y=40+40+50, height=63, width=270)


#button label
btn= tk.Label(root)
btn.place(x=20, y=380, width=620-20-20, height=32)
btn['background']='#add8e6'

sub = tk.Button(btn, width=10, text="Submit",font=("bold"), fg="black", bg="#B6BABA", command= submit)
sub.place(x=20, y=2, width=200, height=25)

back = tk.Button(btn, width=10, text="Back",font=("bold"), fg="black", bg="#B6BABA", command= back)
back.place(x=245, y=2, width=140, height=25)

clear = tk.Button(btn, width=10, text="Clear",font=("bold"), fg="black", bg="#B6BABA", command = clear)
clear.place(x=410, y=2, width=140, height=25)


root.mainloop()