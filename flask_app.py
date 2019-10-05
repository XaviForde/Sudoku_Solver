''' Flask app to run the sudoku solver on Azure Web Apps'''

from flask import Flask, make_response

import numpy as np
import cv2
import time
import transform as tf 


app = Flask(__name__)

@app.route("/")
def hello2():
    return "Hello, sir" #, hello()

'''
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#@app.route("/")
def hello():
    # Create video object to read frames from
    cap = cv2.VideoCapture(0)

    time_start = time.time()

    while time.time() - time_start < 30:
        
        #Read in frame from video object
        ret, img = cap.read()

        #Convert to gray, used for final output
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        cv2.imshow('Gray', imgGray)
        #Pre process image:
        imgBlur = cv2.GaussianBlur(img,(3,3),0)       #Apply blur
        imgBlurGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)     #Convert blurred image to gray

        #Find edges 
        edges = cv2.Canny(imgBlurGray,0,100,apertureSize = 3)  #Fin

        #Find largest contour from the egdes, assumed this is the outer sudoku box
        mask = cv2.inRange(edges, 254,255)
        _,contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        outer_box = max(contours, key = cv2.contourArea)

        peri = cv2.arcLength(outer_box, True)   #perimeter
        approx = cv2.approxPolyDP(outer_box, 0.02 * peri, True) #approximate polygon of contour

        if len(approx) == 4:

            warped = tf.four_point_transform(imgGray.copy(), approx.reshape(4, 2))
            #output = four_point_transform(image, displayCnt.reshape(4, 2))
            # draw the book contour  and display to see if correct

            #Isolate the sudoko puzzle
            #output = imgGray[y:(y+h), x:(x+w)]

            output = warped.copy()

            w_cell = 40 #Width of each cell in the sudoku
            output = cv2.resize(output, (9*w_cell+1,9*w_cell+1))

            for row in range(0,9):
                for col in range(0,9):
                    x_start = 2+row*w_cell
                    y_start = 2+col*w_cell
                    x_end = x_start + w_cell - 4
                    y_end = y_start + w_cell - 4
                    cv2.rectangle(output, (x_start,y_start), (x_end, y_end), color=(255), thickness=1)


            cv2.imshow('out', output)

            #Quit when esc key is pressed:
            key = cv2.waitKey(25)   #25
            if key == 27:
                cv2.imwrite('sudoku2.png', output)
                break


    #Release video capture / destroy open windows:
    cap.release()
    cv2.destroyAllWindows()
    '''

