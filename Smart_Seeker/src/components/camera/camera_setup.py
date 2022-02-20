import cv2


# Set up cascade classifiers
faceCascade = cv2.CascadeClassifier('/home/pi/python/Smart_Seeker/machine-learning/models/face_detection/faceCascade.xml')
fistCascade = cv2.CascadeClassifier('/home/pi/python/Smart_Seeker/machine-learning/models/hand_detection/fist.xml')
fingersCascade = cv2.CascadeClassifier('/home/pi/python/Smart_Seeker/machine-learning/models/hand_detection/fingers.xml')

# Set up camera
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)