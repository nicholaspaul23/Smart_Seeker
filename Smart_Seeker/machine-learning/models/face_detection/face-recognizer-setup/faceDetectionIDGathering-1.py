import cv2
import os
#Part 1
#This code will gather 30 images of 1 user to use as training data in faceDetectionTraining.py

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('faceCascade.xml') #classifier that uses a cascade of simple features to quickly detect faces

# For each person, enter one numeric face id
face_id = input('\n enter user # id end press <return> ==>  ') #this is like a cin >>

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):
    ret, img = cam.read() #read camera gather image
    img = cv2.flip(img, 1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert image color to gray
    faces = face_detector.detectMultiScale(gray, 1.3, 5) #this is a classifier function that will detect multiple faces in the frame
    #parameters include the gray image we just captured, scale factor, and min number of neighbors
    
    
    #next, if faces were found create a rectangle over them, and count faces
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("faceRecData/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
cam.release()
cv2.destroyAllWindows()