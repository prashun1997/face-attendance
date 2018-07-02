from tkinter import *
from docx import Document
from functools import partial
from PIL import Image, ImageTk
import os
import study
import recognise
import webcam
import pickle
import sqlite3 as sq
import time

# Connecting to database server
con=sq.connect('attendance.db')


# Module for switching between different frames
def raise_frame(frame):
    frame.tkraise()

# Module for faculty login
def login():
    global user
    global passw
    global lab
    userid=user.get()
    password=passw.get()
    cursor=con.execute('Select ID,password from faculty')
    u=int(userid)
    flag=0
    for row in cursor:
        if(row[0]==u and row[1]==password):
            flag=1
            break
    if (flag==1):
        raise_frame(f3)
    else:
        lab['text']='Incorrect credentials'

# Unpickling the saved information of students as subjects an their roll numbers.
with open("subjects.txt", "rb") as fp:  # Unpickling
    subjects = pickle.load(fp)

with open("roll.txt", "rb") as fp:  # Unpickling
    rolln = pickle.load(fp)

#Training the newly added students against face recognition

def training(s,r,sec,window):
    global user
    subjects.append(s)
    roll=int(r)
    rolln.append(r)

    with open("subjects.txt", "wb") as fp:
        pickle.dump(subjects, fp)

    with open("roll.txt", "wb") as fp:
        pickle.dump(rolln, fp)

    cursor=con.execute('Insert into student values(?,?,?,?,?)',(roll,s,sec,0,int(user.get())))
    con.commit()
    study.start()#Calling the start fuction from the study module
    window.destroy()



#Running the webcam for face detection
def run():
    l=len(subjects)
    os.mkdir("training-data/s"+str(l))
    webcam.runCam("training-data/s"+str(l)+"/")

#Creating a top level window for adding names of new students
def create_window():
    window = Toplevel(root)
    window.title("Add student info")
    window.geometry("400x250")
    name = Label(window, text="NAME")
    entry = Entry(window, width=20)
    roll = Label(window, text="Class Roll No.")
    number = Entry(window, width=20)
    sec= Label(window, text="Section")
    secw = Entry(window, width=20)
    name.grid(row=1, column=1, pady=10, padx=10)
    entry.grid(row=1, column=2, pady=10)
    roll.grid(row=2, column=1, pady=10, padx=10)
    number.grid(row=2, column=2, pady=10)
    sec.grid(row=3, column=1, pady=10, padx=10)
    secw.grid(row=3, column=2, pady=10)

    info = Message(window,
                   text="Add atleast 10 images for the training set by clicking space when the webcamera starts and press Esc to quit the webcam.",
                   width=350)
    info.grid(row=4, column=1, columnspan=10)

    lab = Button(window, text="Start Webcam", bg="#98FB98", height=1, width=10, pady=10, padx=5, command=run)
    save = Button(window, text="Save", bg="#98FB98", height=1, width=10, pady=10, padx=5, command=lambda: training(entry.get(),number.get(),secw.get(),window))
    save.grid(row=5, column=2)
    lab.grid(row=5, column=1)

#opening attendance sheet of a particular faculty
def getResult():
    global user
    os.startfile('Attendance-sheets\\'+user.get()+'.docx');


#Marking the attendance of students
def mark():
    global id
    person=recognise.start()
    print "Person",person
    cursor=con.execute('Select attendance from student where name="'+person+'"')
    attend=0
    for row in cursor:
        attend=str(int(row[0])+1)
    con.execute('Update student set attendance=? where name=?',(attend,person))
    con.commit()

#Signing up a new faculty member
def signup():
    global namew2,passw2,user2,depw2,cpassw2,lab2
    pass1=passw2.get()
    pass2=cpassw2.get()
    if (pass1!=pass2):
        lab2['text']="Password mismatched"
    else:
        name=namw2.get()
        id=user2.get()
        dep=depw2.get()
        password=passw2.get()
        cursor=con.execute('Insert into faculty values(?,?,?,?)',(id,name,dep,password))
        con.commit()
        document=Document()
        document.save('Attendance-sheets/'+id+'.docx')
        raise_frame(f1)

#Displaying the number of classes attended for a particular student
def show(roll,sec):
    global showlab
    rolln=int(roll)
    cursor = con.execute('Select attendance from student where roll=? and sec=?',(rolln,sec))
    attend = ''
    for row in cursor:
        attend=row[0]
    showlab['text']="You have attended "+attend+" classes"

#Switching different frames
def switch():
    raise_frame(f1)


root = Tk()
root.title('GLAMS')
root.geometry("800x500")
root.configure(background='white')


f0=Frame(root)
f1 = Frame(root,background='white')
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

#Stacking up different frames on a grid
for frame in (f0,f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

#frame1 data
img = ImageTk.PhotoImage(Image.open('gla.jpg'))
pic = Label(f1, image=img).grid(row=1,rowspan=20,columnspan=20)
uname=Label(f1,text='Faculty ID:',font=("Courier", 20),bg='white').grid(row=16,column=3)
user=Entry(f1,width=30)
user.grid(row=16,column=4)
passl=Label(f1,text='Password:',font=("Courier", 20),bg='white').grid(row=17,column=3)
passw=Entry(f1,width=30,show='*')
passw.grid(row=17,column=4)
Button(f1, text='Log In', command=login).grid(row=18,column=3)
Button(f1, text='Sign Up', command=lambda:raise_frame(f2)).grid(row=18,column=4)
lab=Label(f1,font=("Courier", 10),fg='red')
lab.grid(row=19,columnspan=5)
train = Button(f1, text="Click here for Student Login", bg="white", command=lambda:raise_frame(f4),height=2, width=40,font=("Courier", 20),borderwidth=0).grid(row=21,columnspan=10)

#frame2 data
imgback = ImageTk.PhotoImage(Image.open('download.jpg'))
img2 = ImageTk.PhotoImage(Image.open('gla2.jpg'))
Label(f2, text='FRAME 2',image=img2).grid(row=1,rowspan=20,columnspan=20)
uname2=Label(f2,text='Faculty ID:',font=("Courier", 20),bg='white').grid(row=6,column=3)
user2=Entry(f2,width=30)
user2.grid(row=6,column=4)
nam2=Label(f2,text='Name:',font=("Courier", 20),bg='white').grid(row=7,column=3)
namw2=Entry(f2,width=30)
namw2.grid(row=7,column=4)
dep2=Label(f2,text='Department:',font=("Courier", 20),bg='white').grid(row=8,column=3)
depw2=Entry(f2,width=30)
depw2.grid(row=8,column=4)
passl2=Label(f2,text='Password:',font=("Courier", 20),bg='white').grid(row=9,column=3)
passw2=Entry(f2,width=30,show='*')
passw2.grid(row=9,column=4)
cpassl2=Label(f2,text='Confirm Password:',font=("Courier", 20),bg='white').grid(row=10,column=3)
cpassw2=Entry(f2,width=30,show='*')
cpassw2.grid(row=10,column=4)
Button(f2, text='Submit', bg="#98FB98", height=2, width=15, command=signup).grid(row=11,column=4)
Button(f2,image=imgback,command=switch).grid(row=2,column=2)
lab2=Label(f2,font=("Courier", 10),fg='red')
lab2.grid(row=19,columnspan=5)


#frame3
img3 = ImageTk.PhotoImage(Image.open('gla.jpg'))
pic3 = Label(f3, image=img3).grid(row=1,rowspan=15,columnspan=20)
train = Button(f3, text="Student Register", bg="#98FB98", height=2, width=15, command=create_window)
mark = Button(f3, text="Mark Attendance", bg="#98FB98", height=2, width=15,command=mark)
result = Button(f3, text="Attendance Sheet", bg="#98FB98", height=2, width=15,command=getResult)
train.grid(row=20, column=0, padx=60, pady=10)
mark.grid(row=20, column=1, padx=60, pady=10)
result.grid(row=20, column=2, padx=60, pady=10)



#frame4
img4 = ImageTk.PhotoImage(Image.open('gla.jpg'))
pic4 = Label(f4, image=img).grid(row=1,rowspan=20,columnspan=20)
rolll4=Label(f4,text='Roll No.',font=("Courier", 20),bg='white').grid(row=16,column=3)
roll4=Entry(f4,width=30)
roll4.grid(row=16,column=4)
secl4=Label(f4,text='Section',font=("Courier", 20),bg='white').grid(row=17,column=3)
sec4=Entry(f4,width=30)
sec4.grid(row=17,column=4)
Button(f4, text='Get Attendance', command=lambda:show(roll4.get(),sec4.get())).grid(row=18,column=3)
showlab=Label(f4,font=("Courier", 15),bg='white')
showlab.grid(row=19,columnspan=15)
Button(f4,image=imgback,command=switch).grid(row=2,column=2)

#frame0
imgx = ImageTk.PhotoImage(Image.open('splash.jpg'))
Label(f0,image=imgx).grid(row=1,rowspan=15,columnspan=20)
Button(f0,text="GO",command=lambda:raise_frame(f1),font=("Courier", 20),width=10,bg="#98FB98",height=2).grid(row=20,column=10)
raise_frame(f0)


root.mainloop()