import cv2
import numpy as np

#Link our classifiers
palmCascade = cv2.CascadeClassifier('palm.xml')
fingersCascade = cv2.CascadeClassifier('fingers.xml')

#Start video capture
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

#Loop for constant feed

while True:
    #read in video, store in img
    ret, img = cap.read()
    img = cv2.flip(img,1) #flip camera output
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert color to grayscale
    
    #detect features
    palm = palmCascade.detectMultiScale(gray, 1.1, 150)
    fingers = fingersCascade.detectMultiScale(gray, 1.1, 150)
    
    #create the frame for detected gestures
    for(x,y,w,h) in palm:
        cv2.rectangle(img, (x,y), (x+w,y+h), (250,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]
        cv2.putText(img, "palm", (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
       
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    '''
    for(x,y,w,h) in fingers:
        cv2.rectangle(img, (x,y), (x+w,y+h), (250,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]
        cv2.putText(img, "fingers", (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    '''   
        