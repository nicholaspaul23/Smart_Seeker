import numpy as np
import cv2

faceCascade = cv2.CascadeClassifier('faceCascade.xml') # import cascade filesheet for face detection

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1) # -1 to flip video upside down
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # read in data as gray for cascade algorithim to handle
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    ) # call the cascade classifier function pasing paramaters gray for input, scale factor for how much the image size is reduced
    # at each image scale to create scale pyramid, minNeighbors for how many neighbors each canditate rectangle should have
    # (higher number gives lower false positives), and minSize rectangle should consider a face

    # if a face is found return position (x,y) of left upper corner along with
    # width and height
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]  

    cv2.imshow('video',img) # once we get the locations we can create a ROI (drawn rectangle) for the face and present it

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()