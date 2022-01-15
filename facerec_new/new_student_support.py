import os
import face_recognition
import numpy as np
import codecs, json
import numpy
from json import JSONEncoder
import pyrebase
import google.cloud
import firebase_admin
from firebase_admin import credentials,firestore

path = os.getcwd()
with os.scandir(f"{path}/db") as listOfEntries:
	for entry in listOfEntries:
		if (entry.is_file() and entry.name.endswith(".json")):
   			path = f"./db/{entry.name}"

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def stData_local(filename,known_fname,known_lname,adm_no,cs):

	known_image = face_recognition.load_image_file(filename)
	known_face_encoding = face_recognition.face_encodings(known_image)[0]

	known_file = {}
	
	known_file["known_encoding"] = known_face_encoding
	known_file["known_fname"] = known_fname
	known_file["known_id"] = adm_no
	known_file["class"] = cs

	# Serialization

	with open(f"known_students_data/{adm_no}.json", "w") as write_file:
		json.dump(known_file, write_file, cls=NumpyArrayEncoder)


def stData_database(adm,fname,lname,sn,cs,pno):

	global path
	
	cred = credentials.Certificate(path)
	firebase_admin.initialize_app(cred)
	db = firestore.client()
	data = {
	"first_name" : fname,
	"last_name" : lname,
	"phone_no" : pno,
	"class" : cs
	} 
	data_a={
	"name" : fname+" "+lname
	}

	db.collection("Session").document(sn).collection("Reference").document(adm).set(data)
	db.collection("Android").document(adm).set(data_a)



