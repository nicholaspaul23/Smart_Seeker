from camera_setup import *


#check for fist (stop pursuit)
def findFist():
    ret, img = cap.read()
    img=img[100:346,100:346]
    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fist = fistCascade.detectMultiScale(gray, 1.1, 5)
    fistCount = 0
    for(x,y,w,h) in fist:
        cv2.rectangle(img, (x,y), (x+w,y+h), (250,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]
        fistCount+=1
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if(fistCount > 0):
        return True
    else:
        return False