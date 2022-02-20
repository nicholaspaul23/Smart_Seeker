from camera_setup import *

#read camera for faces
def readCam():
    ret, img = cap.read()
    img = cv2.flip(img, 1) # -1 to flip video upside down
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) 
    cv2.imshow('video',img) # once we get the locations we can create a ROI (drawn rectangle) for the face and present it
    k = cv2.waitKey(30) & 0xff
    return faces