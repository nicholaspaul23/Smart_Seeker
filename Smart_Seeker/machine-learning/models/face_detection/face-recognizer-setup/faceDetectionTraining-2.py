import cv2
import numpy as np
from PIL import Image
import os
#Part 2
# ! Everytime faceDetectionIDGatherin.py is run this must also be run
# This program will take all photos in faceRecData folder and subfolders returning two arrays Ids and Faces that will train our
# recognizer and will be stored in trainer.yml

'''
we are taking the images gathered
-grabbing the paths of the image to parse the user id out
-store user id in array

-detect faces in each image
-store the face image in another array

-then pass the user ids along side the face array to the recognizer
to create a training yml file

'''


# Path for face image database
path = 'faceRecData'

recognizer = cv2.face.LBPHFaceRecognizer_create()
# this is a recognizer Local binary patterns histograms recognizer included in OpenCV
detector = cv2.CascadeClassifier("faceCascade.xml");

#The function "getImagesAndLabels (path)", will take all photos on directory: "dataset/", returning 2 arrays: "Ids" and "faces". With those arrays as input, we will "train our recognizer":
# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     #this will parse the path of the image folder and get parent directories to get absolute path
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])    #parse the id of image out of the image path
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

print ("\n Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))