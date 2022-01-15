#!/usr/bin/python
import tkinter as tk
from tkinter import *
from subprocess import *
import tkinter, time
import face_recognition
import cv2
import numpy as np
import json
import os
import numpy
from PIL import ImageTk, Image
import pyrebase
import google.cloud
import firebase_admin
from firebase_admin import credentials,firestore
from datetime import *


presents ={}
video_capture = None
videoLabel = None

def begin():
	startVideoCapture()
	try:
		top.destroy()
	except:
		pass

def startVideoCapture():

	global video_capture
	video_capture = cv2.VideoCapture(0)
	# Initialize some variables
	global presents
	face_locations = []
	face_encodings = []
	face_names = [] 
	process_this_frame = True

	while True:
		face_names = {}
		ret, frame = video_capture.read()
		if ret:
			small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
		else:
			continue
		rgb_small_frame = small_frame[:, :, ::-1]

		#if process_this_frame==0:
		if process_this_frame:
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			face_names = []
			for face_encoding in face_encodings:
				matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
				name = "Unknown"

				face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
				best_match_index = np.argmin(face_distances)
				if matches[best_match_index]:
					name = known_face_names[best_match_index]
				face_names.append(name)

		#process_this_frame = not process_this_frame
		#process_this_frame+=1
		#process_this_frame%=4
    # Display the results
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4
			if(name=='Unknown'):
				B=0
				G=0
				R=255
				shade=255
			else:
				B=0
				G=255
				R=0
				shade=0
        # Draw a box around the face
        # Draw a label with a name below the face
			cv2.rectangle(frame, (left, top), (right, bottom), (B, G, R), 2)
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (B, G, R), cv2.FILLED)
			
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (shade, shade, shade), 1)
			if(name!='Unknown'):
				presents[known_face_ids[best_match_index]] = (known_face_names[best_match_index],known_face_class[best_match_index])

		cv2.imshow('Video, press "q" to stop video', cv2.resize(frame, (854, 480)))
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	video_capture.release()
	cv2.destroyAllWindows()

def check_presents():
	now=datetime.now()
	global presents
	global videoLabel
	date = str(now.day)+'/'+str(now.month)+'/'+str(now.year)
	time = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
	no_presents = str(len(presents))
	doc="""	
Date :- """+date+"""


Number of student Present :- """+no_presents+"""


Time :- """+time
	videoLabel.config(text =doc,font=("Helvetica",18,"bold"),padx=20,pady=20,anchor = 'nw', justify =LEFT)


def func():
    proc = Popen("new_student_page.py", stdout=PIPE, shell=True)
    proc = proc.communicate()

def gui():
	#gui
	global videoLabel
	top = tkinter.Tk()
	top.title('Attendance_System')
	top.geometry('700x385') # Size 200, 200
	top['background']='#add8e6'


	footer = tk.Label(top,relief=tk.RIDGE)
	footer['background']='#add8e6'
	footer.place(x = 500, y = 30 , height=330, width=180)

	markAttendance = tkinter.Button(footer, height=2, width=20, text ="Mark Attendance",font="bold", command = mark)

	addNewStudent = tkinter.Button(footer, height=2, width=20, text ="Add New Student",font="bold", command = func) 

	presentStudents = tkinter.Button(footer, height=2, width=20, text ="Present Students",font="bold", command = check_presents) 

	startButton = tkinter.Button(footer, height=2, width=20, text ="Start",font="bold", command = begin)

	videoLabel = tkinter.Label(top, relief=tk.RIDGE)

	startButton.place(x=10,y=20,width=160,height=40)
	presentStudents.place(x=10,y=20+80,width=160,height=40)
	markAttendance.place(x=10,y=20+80+80,width=160,height=40)
	addNewStudent.place(x=10,y=20+80+80+80,width=160,height=40)
	videoLabel.place(x=10, y=30, height=330, width=474)
	top.mainloop()


def mark():
	global videoLabel
	now = datetime.now()
	cred = credentials.Certificate(path)
	firebase_admin.initialize_app(cred)
	db = firestore.client()
	try:
		for x in presents:
			data = {
			"First_name" : presents[x][0],
			"Roll_no" : x
			}
			data_a = {
			"day" : str(now.day),
			"status" : "present"
			}
			db.collection("Session").document(str(now.year)).collection("Class").document(str(presents[x][1])).collection("Month").document(str(now.month)).collection("Date").document(str(now.day)).collection("Presents").document(x).set(data)
			db.collection("Android").document(x).collection("Session").document(str(now.year)).collection("Month").document(str(now.month)).collection("Date").document(str(now.day)).set(data_a)
		videoLabel.config(text ="	Attendence is Marked",font=("Helvetica",18,"bold"),padx=10,pady=40,anchor = 'nw', justify =LEFT)
	except:
		videoLabel.config(text ="	No Attendance is Marked",font=("Helvetica",18,"bold"),padx=10,pady=40,anchor = 'nw', justify =LEFT)

if __name__=="__main__":
	running = True  
	Freq = 2500
	Dur = 150
	path = os.getcwd()

	with os.scandir(f"{path}/db") as listOfEntries:
		for entry in listOfEntries:
			if (entry.is_file() and entry.name.endswith(".json")):
	   			path = f"./db/{entry.name}"


	#pre data loading
	known_face_encodings = []
	known_face_names = []
	known_face_ids = []
	known_face_class = []

	print("Started Reading JSON file")

	for filename in [file for file in os.listdir("known_students_data/") if file.endswith(".json")]:


		with open("known_students_data/"+filename, "r") as read_file:
			print("Converting JSON encoded data into Numpy array")
			ret_file = json.load(read_file)
	        
		ret_file.update({"known_encoding": numpy.asarray(ret_file["known_encoding"]) })

		known_face_encodings.append(numpy.asarray(ret_file["known_encoding"]))
		known_face_ids.append(ret_file["known_id"])
		known_face_names.append(ret_file["known_fname"])
		known_face_class.append(ret_file["class"])

		
		#p1 = multiprocessing.Process(target=gui)
		#p1.start()

	gui()

	print(presents)