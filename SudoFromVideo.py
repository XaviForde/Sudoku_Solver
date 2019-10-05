# This takes live video stream from webcam and 
# isolates the sudoku puzzle in the image
# where the ouput is a square image containing
# only the sudoku

import numpy as np
import cv2
import pandas as pd
import transform as tf 
import matplotlib.pyplot as plt


def getSudokuImage(img):
    
    #Convert to gray, used for final output
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    output = np.array([])
    
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

    #Apply check to see if it the outer sudoku box
    if len(approx) == 4 and 800 < peri < 1500:

        #Tranform the image to get a square birds eye view of the sudoku
        warped = tf.four_point_transform(imgGray.copy(), approx.reshape(4, 2))
        output = warped.copy()

        w_cell = 40 #Width of each cell in the sudoku
        output = cv2.resize(output, (9*w_cell+1,9*w_cell+1))

        #Draw borders around each cell in the sudoku
        for row in range(0,9):
            for col in range(0,9):
                x_start = 2+row*w_cell
                y_start = 2+col*w_cell
                x_end = x_start + w_cell - 4
                y_end = y_start + w_cell - 4
                cv2.rectangle(output, (x_start,y_start), (x_end, y_end), color=(255), thickness=1)

    return output


def getSudoImages(n_images, cap):

    # Create video capture object
    #cap = cv2.VideoCapture(0)
    #Ensures first framse sudoku is found are not used so there
    #   is time to steady the camera
    stable_cnt = 0

    sudokuImages = np.zeros((9,9,1))

    while sudokuImages.shape[2] != n_images:

        #Read in frame
        _, img = cap.read()
        cv2.imshow('Live Video', img)
        key = cv2.waitKey(25)

        output = getSudokuImage(img)
    
        # If output size is zero sudoku was not found
        if output.size != 0:
            cv2.imshow('out', output)
            stable_cnt += 1
            if stable_cnt == 1:
                sudokuImages = np.zeros((output.shape[0],output.shape[1],1))
                sudokuImages[:,:,0] = output
                isFirst = False
            
            elif stable_cnt > 1 and stable_cnt % 2 == 0:
                sudokuImages = np.append(sudokuImages, output[:,:,np.newaxis], axis=2)
                
   
    #Release video capture / destroy open windows:
    # cap.release()
    # cv2.destroyAllWindows()
    return sudokuImages, cap
                       


        # #Quit when esc key is pressed:
        # key = cv2.waitKey(25)   
        # if key == 27: # 27 = esc
        #     break



