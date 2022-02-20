from camera_setup import *


#check for fingers (Okay go)
def findFingers():
    ret, img = cap.read()
    img=img[100:346,100:346]
    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fingers = fingersCascade.detectMultiScale(gray, 1.1, 150)
    fingersCount = 0
    for(x,y,w,h) in fingers:
        cv2.rectangle(img, (x,y), (x+w,y+h), (250,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]
        fingersCount+=1
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if(fingersCount > 0):
        return True
    else:
        return False