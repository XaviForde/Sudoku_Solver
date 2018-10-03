###About this file

# I hope this will solve easy sudoku problems
# Input is a 9x9 array representing the sudoku puzzle with 0 representing blank spaces
# Future work will be to have image input instad of manual

######

import numpy as np
import pandas as pd

#Input sudoku, can be found at following link: https://www.websudoku.com/?level=1&set_id=3126256010

sudo = np.array([[1, 0, 0, 0, 0, 4, 0, 8 ,0],
         [7, 5, 0, 9, 2, 0, 0, 0, 0], 
         [0, 0, 0, 5, 0, 6, 0, 0, 3],
         [0, 0, 0, 0, 6, 0, 5, 7, 0],     
         [3, 7, 0, 0, 8, 0, 0, 6, 4],
         [0, 8, 6, 0, 9, 0, 0, 0, 0],
         [8, 0, 0, 1, 0, 9, 0, 0 ,0],      
         [0, 0, 0, 0, 4, 2, 0, 5, 9],
         [0, 4, 0, 6, 0, 0, 0, 0, 1]])    #last row


class cell:
    def __init__(self, r, c, sudo = sudo):
        self.r = r
        self.c = c
        self.row = set(sudo[r,:])
        self.col = set(sudo[:,c])
        self.value = sudo[r,c]
    
    #Method to determine if the cell has a number assigned
    def isempty(self):
        if self.value == 0:
            return True
        else:
            return False
    
    #Method to return the 3x3 box the cell is in
    def get_box(self):
        r = self.r
        c = self.c

        if r == 0 or r == 1 or r == 2:
            if c == 0 or c == 1 or c == 2:
                return sudo[0:3, 0:3]
            elif c == 3 or c == 4 or c == 5:
                return sudo[0:3, 3:6]
            elif c == 6 or c == 7 or c == 8:
                return sudo[0:3, 6:9]
    
        elif r == 3 or r == 4 or r == 5:
            if c == 0 or c == 1 or c == 2:
                return sudo[3:6, 0:3]
            elif c == 3 or c == 4 or c == 5:
                return sudo[3:6, 3:6]
            elif c == 6 or c == 7 or c == 8:
                return sudo[3:6, 6:9]
        
        elif r == 6 or r == 7 or r == 8:
            if c == 0 or c == 1 or c == 2:
                return sudo[6:9, 0:3]
            elif c == 3 or c == 4 or c == 5:
                return sudo[6:9, 3:6]
            elif c == 6 or c == 7 or c == 8:
                return sudo[6:9, 6:9]

        #Method to determine numbers cell can not take as they are used in the row, column or box
    def taken_nums(self):
        used_nums = []
        box = self.get_box()
        for num in range(1,10):
            if num in self.row:
                    used_nums.append(num)
            if num in self.col:
                    used_nums.append(num)
            if num in box:
                    used_nums.append(num)                
            else:
                pass
                
        used_nums = set(used_nums)
        return used_nums

options_list = []

#Iterate over the simple solver until either sudoku is complete or
#there is no change from the previous iteration of sudo (i.e. need another method to solve)

while 0 in sudo:
#Iterate over cells and find possible values
#If only one possible value then place into sudo
    prev_sudo = sudo.copy()
    change_count = 0
    for r in range (0,9):
        for c in range (0,9):
            
            iter_cell = cell(r,c)
            if iter_cell.isempty() == False:                #If there is already a number assigned to the cell
                options_list.append([sudo[r,c]])
            elif iter_cell.isempty() == True:
                nums_used = set(iter_cell.taken_nums())
                nums_available = []
                for num in range (1,10):
                    if num in nums_used:
                        pass
                    else:
                        nums_available.append(num)
                if len(nums_available) == 1:                #If only one solution then add it to the sudo
                    sudo[r,c] = nums_available[0]
                    change_count += 1
                options_list.append(nums_available)

    if change_count == 0:
        print('Could not be solve using simple method, options are:')
        break

options_mdarray = np.array(options_list)
print(options_mdarray)






#print(options_mdarr)