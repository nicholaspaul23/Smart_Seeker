# Smart Seeker

This AI robot utilizes computer vision, machine learning and sensors to navigate its environment detect a user and respond to the user’s gestures for commands. This robot will first search for a user and upon face detection it will begin to pursue the user. It will use its obstacle avoidance protocol to navigate around its environment and get on course to meet its user. The robot will respond to hand gestures such as the “stop” and “peace” sign to stop itself or keep going to purse the user.  This robot utilizes OpenCV and uses convolutional neural network cascade classifiers to detect users faces. Further implementation allows users to train the robot to recognize their face upon detection. An additional classification model is used to detect the user’s hand gestures. Using infrared and ultrasonic sensors the robot can map and detect objects in its path. If an object is in its path, the robot will try to estimate its size while trying to avoid it. Once the object is avoided it will run a protocol to get the robot repositioned back to its original path/course to the detected user. 


https://user-images.githubusercontent.com/47327154/154851810-96df04ff-b5ff-4c01-871e-ed044c6826fe.MOV


https://user-images.githubusercontent.com/47327154/154851816-cf7cf37f-4403-4dcc-a1b0-9c130b4a5acf.MOV

