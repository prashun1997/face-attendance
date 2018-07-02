# face-attendance
Attendance Marking System Using Face Recognition

<h3>Overview</h3>

With advancement in technologies of computer vision the old traditional method of marking attendance of students by calling out their roll numbers can be replaced with a face recognition based attendance marking system which would be highly convenient both for the professor and student.

Software Requirements
-------------------
Python 2.7 environment with modules like cv2(Open-CV), numpy, Tkinter, pickle and PIL installed.

USAGE
------
The `gui.py` is the main application file through which you would run the application. Opening the application you would get an interactive window where the faculties could log in with their credentials to mark the attendance of students, view the attendace sheet and register a new student. A new faculty could sign up with their details. There is a student login where students can view the number of classes they have attended by entering their roll numbers and section.

The folder `training_data` will contain the images of students that have been signed by their faculties. For each student their will be a separate folder that would contain about 10 of its photos clicked by the camera during the registration time. The `study.py` is the file that performs a study of all the present images in the `training_data` folder whenever a new student is added. This is done to detect faces and their labels and store the same information in faces2.txt and labels2.txt.    

The `recognise.py` helps the application in marking the attendace by recognising the face and internally updating the attendance in the database and the attendace sheet of the respective faculty.


WORKING PRINCIPLE
---------------------
We have used the OpenCV cv2 module for python. OpenCV comes equipped with built in face recognizer, all you have to do is feed it the face data. We use the LBPH face recogniser. The idea is to not look at the image as a whole instead find the local features of an image. LBPH alogrithm try to find the local structure of an image and it does that by comparing each pixel with its neighboring pixels. Take a 3x3 window and move it one image, at each move (each local part of an image), compare the pixel at the center with its neighbor pixels. The neighbors with intensity value less than or equal to center pixel are denoted by 1 and others by 0. Then you read these 0/1 values under 3x3 window in a clockwise order and you will have a binary pattern like 11100011 and this pattern is local to some area of the image. You do this on whole image and you will have a list of local binary patterns. After you get a list of local binary patterns, you convert each binary pattern into a decimal number (as shown in above image) and then you make a histogram of all of those values. 
Later during recognition, when you will feed a new image to the recognizer for recognition it will generate a histogram for that new image, compare that histogram with the histograms it already has, find the best match histogram and return the person label associated with that best match histogram. 

Applications & Future Scope
----------------------------
The application finds utility in colleges where much time is spent in every class marking the attendace of the student. This could replace the traditional way and would be time efficient. Depth sensing could be added for better recognition of person. I created this application in view of my university, people are welcome to modify their code suiting their requirements.

<br><br>
PS: The application won't work in distinguishing twins..:stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye:

Hope you will enjoy running the applcation and you will find it informative to learn about computer vision and its scope.
