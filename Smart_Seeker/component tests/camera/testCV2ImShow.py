import cv2

faceCascade = cv2.CascadeClassifier('faceCascade.xml') # import cascade filesheet for face detection

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

while(True):
    ret, img = cap.read()
    cv2.imshow('frame',img)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()