import numpy as np
import math
from scipy import stats
import cv2
import pandas as pd
from sklearn import datasets, svm, metrics
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import joblib
import SudoFromVideo as vid
import sudoku_solver as solver

    #Create the SVC digit classifier
def CreateTrainSaveClassifier():
    # Load the digits dataset: digits
    digits = datasets.load_digits()

    #Reformat by flatenning the arrays
    n_samples = len(digits['images'])
    image_data = digits['images'].reshape((n_samples, -1)) #flatten the image arrays

    #Create the 'support vector classifier' object
    svc = svm.SVC(gamma=0.001, C=100)

    #Train the classifier on the dataset
    svc.fit(image_data, digits['target']) 

    #Save the classifier 
    joblib.dump(svc, 'model_scv_1.pkl')


# Read digits 
# clf = classifier object
# sudoImg = gray image of the sudoku
# w_cell = width of cell in pixels
def ReadSudokuDigits(clf, sudoImg, w_cell):
    
    #Initialize array to represent the sudoku
    sudo_arr = np.zeros((9,9))

    for col in range(0,9):
        for row in range(0,9):

            #Get the cell
            x_start = 4+col*w_cell
            y_start = 4+row*w_cell
            x_end = x_start + w_cell - 6
            y_end = y_start + w_cell - 6
            cellImg = sudoImg[y_start:y_end,x_start:x_end]

            #Check if empty
            isEmpty = EmptyCheck(cellImg)
            if isEmpty:
                continue
            
            else:
                digit_pred = PredictDigit(clf, cellImg)
                sudo_arr[row,col] = int(digit_pred)
    return sudo_arr

def EmptyCheck(cellImg):

    # Get central area
    width = cellImg.shape[0] // 2
    check_area = cellImg[(width-10):(width+10),(width-10):(width+10)]
    #Improve next line by subracting min from max
    isEmpty = True if (check_area.max() - check_area.min()) <=40 else False

    return isEmpty

def PredictDigit(clf, cellImg):

    #cv2.imshow('Cell', cellImg )
    #Apply threshold to isolate black text
    mask = cv2.adaptiveThreshold(cellImg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    mask = 255 - mask
    #Find contours and retrieve largest
    _,contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    digit_bounds = max(contours, key = cv2.contourArea) #bounding contour

    #Get bounding contour corners as a square
    x,y,w,h = cv2.boundingRect(digit_bounds)    #Bounding rectange
    centre = [int(x+(w/2)),int(y+(h/2))]    #centre point
    max_len = math.ceil(max(w,h) / 2)   #longest side
    start = (abs(centre[0]-max_len), abs(centre[1]-max_len))    #start coords
    end = (centre[0]+max_len, centre[1]+max_len)    #end coords

    cell_copy = cellImg.copy()
    cv2.rectangle(cell_copy,start,end,(255),1)
    #cv2.imshow('Box', cell_copy)

    cell_digit = cellImg[start[1]:end[1], start[0]:end[0]]
    cell_digit = cv2.resize(cell_digit,(8,8))
    #key = cv2.waitKey(0)

    #Convert to array, scale between 0 and 255 and flatten
    cell_digit = np.asarray(cell_digit, dtype="float64") 
    cell_digit -= cell_digit.min()  #set backgound to 0
    cell_digit *= 16.0/cell_digit.max()    #scale to 0-255
    cell_digit = 16.0*np.ones((8,8)) - cell_digit   #White to black convesion
    #cell_digit[cell_digit < 3 ] = 0.       #set dim pixels to zero
    #cell_digit[cell_digit > 12] = 16.     #set light pixels to 255


    # Uncomment next 2 lines to plot the 28x28 image 
    #plt.imshow(cell_digit, cmap=plt.cm.gray_r, interpolation='nearest')
    #plt.show()

    #Flatten and round array
    cell_digit = cell_digit.flatten()
    cell_digit = np.rint(cell_digit)

    #predict the digit 
    digit_pred = clf.predict(cell_digit.reshape(-1,(8**2)))[0]
    #print('Predicted value is {}.'.format(digit_pred))
    return digit_pred

#Return number of times and empty cell (0) was assigned a number
def emptyFailCount(sudo_actual, sudo_out):
    empty_fail = 0
    for i in range(0,9):
        for j in range(0,9):
            if sudo_actual[i,j] == 0 and sudo_out[i,j] !=0:
                empty_fail += 1
    return empty_fail

#Retruns metrics which show accuracy agains hard coded
#array of the sudoku 
def HardCodedCompar(sudo_actual, sudo_arr, sudo_out):
    #Compare with hard coded solution
    comp_arr = np.array(np.equal(sudo_out, sudo_actual), dtype='int32')
    for i in range(0,9):
        for j in range(0,9):
            if comp_arr[i,j] == 0:
                print('loc = ' + str(i+1) + ',' + str(j+1))
                print(sudo_arr[i,j,:])
    empty_fail = emptyFailCount(sudo_actual, sudo_out)
    print('Zero failure total = {}'.format(empty_fail))
    print('Incorrect classification = {}'.format(81-np.sum(comp_arr)+empty_fail))


def dispSolution(sudo_out, sudo_solved, sudoImg, w_cell):
    
    sudoImg = cv2.cvtColor(sudoImg, cv2.COLOR_GRAY2BGR)
    for i in range(0,9):
        for j in range(0,9):
            if sudo_out[i,j] == 0:
                y = (w_cell // 2) + w_cell*i + 8
                x = (w_cell // 2) + w_cell*j - 8
                digit = str(sudo_solved[i,j])
                sudoImg = cv2.putText(img = sudoImg, 
                                        text = digit, 
                                        org = (x,y), 
                                        fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                                        fontScale = 0.75,
                                        color = (0,255,0),
                                        thickness = 2)
        
    return sudoImg


def checkSudoCorrect(sudo_solved):
    #Assume sudoku is correct initially
    isCorrect = True

    if 0 in sudo_solved:
        isCorrect = False

    if isCorrect == True:
        #Check rows and columns
        for i in range(0,9):
            setCol = set(sudo_solved[:,i])
            setRow = set(sudo_solved[i,:])
            if len(setCol) != 9 or len(setRow) != 9:
                isCorrect = False
                break
        
            if isCorrect == True:
                #Check the boxes
                for i in range(0,3):
                    for j in range(0,3):
                        box = sudo_solved[(i*3):((i+1)*3), (j*3):((j+1)*3)]
                        setBox = set(box.flatten())
                        if len(setBox)!= 9:
                            isCorrect = False

    return isCorrect


#----------------------------------------------
#       Solving the sudoku from webcam video:
#----------------------------------------------

#Load the digit classifier model Support Vector Classification
svc = joblib.load('model_scv_1.pkl')

#Create camera object
cap = cv2.VideoCapture(0)
cap.set(4,360);

while True:

    #Display the video
    _, img = cap.read()
    cv2.imshow('Live Video', img)
    key = cv2.waitKey(25)
    #Read images
    n_images = 3 #number of images to take
    sudoImages, cap = vid.getSudoImages(n_images,cap)

    sudo_arr = np.zeros((9,9,n_images))

    # Classify digits for each image of the sudoku
    for i in range(0,n_images):
        #Classify the digits
        sudoImg = sudoImages[:,:,i]
        sudo_arr[:,:,i] = ReadSudokuDigits(svc, np.array(sudoImg, dtype='uint8'), w_cell=40)

    # Take the modal digit across the images for each cell
    sudo_out, _ = stats.mode(sudo_arr, axis=2)
    sudo_out = sudo_out.reshape((9,9))
    sudo_out = np.array(sudo_out, dtype='int32')

    #print('Unsolved Sudoku:')
    #print(sudo_out)

    #Solve the sudoku
    sudo_solved = solver.SolveSudoku(sudo_out.copy())

    solvedImg = dispSolution(sudo_out.copy(), sudo_solved, np.array(sudoImages[:,:,-1], dtype='uint8'), w_cell=40)

    
    
    if checkSudoCorrect(sudo_solved):
        cv2.imshow('Solved Puzzle', solvedImg)
        key = cv2.waitKey(0)

    #print('Solved Sudoku:')
    #print(sudo_solved)



# cv2.imshow('sudo', output)
# key = cv2.waitKey(0)   #25
