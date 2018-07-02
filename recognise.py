import cv2
import os
import numpy as np
import pickle
from docx import Document
import time
import sqlite3 as sq


def detect_face(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Using local binary pattern as classifier for predicting faces
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(faces) == 0):
        cv2.imshow('Not detected',img)
        cv2.waitKey(100)
        return None, None

    (x, y, w, h) = faces[0]

    return gray[y:y + w, x:x + h], faces[0]


def run():

    faceCascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    global label_text
    global roll
    cam = cv2.VideoCapture(0)
    cam.set(3, 203)
    cam.set(4, 248)
    f=0
    while True:
        # Capture frame-by-frame
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

        k = cv2.waitKey(1)

        # Draw a rectangle around the faces
        for (x,y,w,h) in faces:


            label = face_recognizer.predict(gray[y:y + w, x:x + h])
            print label

            label_text = subjects[label[0]]
            roll=rolln[label[0]]
            print label_text

            f+=1

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & f == 1:
            break



def start():

    global face_recognizer
    global subjects
    global faces
    global labels
    global rolln

    with open("subjects.txt", "rb") as fp:  # Unpickling
        subjects = pickle.load(fp)

    with open("faces2.txt", "rb") as fp:  # Unpickling
        faces = pickle.load(fp)

    with open("labels2.txt", "rb") as fp:  # Unpickling
        labels = pickle.load(fp)

    with open("roll.txt", "rb") as fp:  # Unpickling
        rolln = pickle.load(fp)
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    run()

    con=sq.connect('attendance.db')
    faculty=con.execute('Select faculty from student where name="'+label_text+'";').fetchall()[0][0]
    #Adding the marked attendance
    document = Document('Attendance-sheets/'+str(faculty)+'.docx')

    document.add_paragraph(roll+".       "+label_text+"             " +time.strftime("%c"))
    document.save('Attendance-sheets/'+str(faculty)+'.docx')
    return label_text
