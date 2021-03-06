###
#About this file:

# Currently first layer of logic solves easy problems 
# Second layer of logic solves some additional cells that the first could not
# Input is a 9x9 array representing the sudoku puzzle with 0 representing blank spaces
# Future work will be to have image input instad of manual

######

import numpy as np

#Input sudoku, can be found at following link: https://www.websudoku.com/?level=1&set_id=3126256010

# sudo = np.array([[2, 0, 1, 5, 0, 6, 0, 0 ,0],
#          [8, 0, 0, 2, 0, 0, 5, 0, 1], 
#          [0, 0, 5, 8, 0, 0, 0, 7, 0],
#          [7, 0, 0, 0, 8, 0, 0, 3, 9],     
#          [0, 0, 9, 3, 6, 4, 7, 0, 0],
#          [5, 8, 0, 0, 2, 0, 0, 0, 6],
#          [0, 1, 0, 0, 0, 9, 3, 0 ,0],      
#          [3, 0, 4, 0, 0, 2, 0, 0, 5],
#          [0, 0, 0, 4, 0, 8, 1, 0, 7]])  

# #Define the cell windows
# first_win = [0, 1, 2]
# second_win = [3, 4, 5]
# third_win = [6, 7, 8]

class cell:

    def __init__(self, r, c, sudo):
        self.r = r
        self.c = c
        self.row = set(sudo[r,:])
        self.col = set(sudo[:,c])
        self.value = sudo[r,c]
    
    #Method to determine if the cell has a number assigned
    def isEmpty(self,sudo):
        if sudo[self.r,self.c] == 0:
            return True
        else:
            return False
    
    #Method to determine which box number the cell is in
    def get_box_loc(self):
        row_start = (self.r // 3) * 3
        # Add the box column index to the box row start index to get the box loc
        self.box = row_start + self.c // 3 + 1
    
        return self.box
   
    #Method to return the 3x3 box the cell is in
    def get_box_values(self, sudo):

        row_start = (self.r // 3) * 3
        row_end = row_start + 3
        col_start = (self.c // 3) * 3
        col_end = col_start + 3

        return sudo[row_start:row_end, col_start:col_end]

    #Method to determine numbers cell can not take as they are used in the row, column or box
    def taken_nums(self,sudo):
        used_nums = []
        box = self.get_box_values(sudo)
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
        self.used_nums = used_nums
        return used_nums

    def get_avail_nums(self,sudo):
        if sudo[self.r, self.c] == 0:
            nums_used = set(self.taken_nums(sudo))
            nums_available = []
            for num in range (1,10):
                if num in nums_used:
                    pass
                else:
                    nums_available.append(num)
            self.nums_avail = nums_available
            return nums_available
        else:
            cell_value = [sudo[self.r, self.c]]  
            return cell_value       


def simple_solver(sudo):
    ##First Lyer of Logic
    #Iterate over the simple solver until either sudoku is complete or
    #there is no change from the previous iteration and another method is needed to solve
    options_list = []
    cell_dict = {}
    while 0 in sudo:
    #Iterate over cells and find possible values
    #If only one possible value then place into sudo
        change_count = 0
        dict_index = 0
        
        for r in range (0,9):           
            for c in range (0,9):
                
                cell_dict[dict_index] = cell(r,c, sudo)
                dict_index += 1
                if cell_dict[dict_index-1].isEmpty(sudo) == False:                  #Check if cell solved, if so add cell value to options list
                    options_list.append([sudo[r,c]])                            
                elif cell_dict[dict_index-1].isEmpty(sudo) == True:
                    nums_available = cell_dict[dict_index-1].get_avail_nums(sudo)
                
                    if len(nums_available) == 1:                
                        sudo[r,c] = nums_available[0]
                        change_count += 1
                    options_list.append(nums_available)

        if change_count == 0:
            print(sudo)
            print('More trickery is needed to solve this one...')
            break
    
    return cell_dict, sudo

def unique_poss_solver(cell_dict, sudo): 
    while 0 in sudo:
    
        change_count = 0
        for i in range(0,81):
            if len(cell_dict[i].get_avail_nums(sudo)) != 1:             #if length of nums available is not 1 then the cell must be solved 
        
                cell_options = cell_dict[i].get_avail_nums(sudo)        #get options for the cell
                row_options = []                                #empty array for all the other options in the row
                col_options = []                                #empty array for all the other options in the col
                box_options = []                                #empty array for all the other options in the box
                row = cell_dict[i].r
                col = cell_dict[i].c
                box = cell_dict[i].get_box_loc()
                for ii in range(0,81):                     #get other options in the row, col and box in separate arrays
                
                    if ii != i:                              #dont want to add cell we are trying to solve into other options
                        if cell_dict[ii].r == row:
                            row_options.append(cell_dict[ii].get_avail_nums(sudo))
                        if cell_dict[ii].c == col:
                            col_options.append(cell_dict[ii].get_avail_nums(sudo))
                        if cell_dict[ii].get_box_loc() == box:
                            col_options.append(cell_dict[ii].get_avail_nums(sudo))
                        
                row_diff = set(cell_options) - set([item for sublist in row_options for item in sublist])       #finds if there is a unique solution to cell in row
                col_diff = set(cell_options) - set([item for sublist in col_options for item in sublist])       #finds if there is a unique solution to cell in column
                box_diff = set(cell_options) - set([item for sublist in box_options for item in sublist])       #finds if there is a unique solution to cell in box
                
                if len(row_diff) == 1:
                    x = list(row_diff)[0]
                    sudo[row,col] = x
                    change_count =+ 1
                elif len(col_diff) == 1:
                    x = list(col_diff)[0]
                    sudo[row,col] = x
                    change_count =+ 1
                elif len(box_diff) == 1:
                    x = list(box_diff)[0]
                    sudo[row,col] = x
                    change_count =+ 1

        if change_count == 0:
            print('This is going to require taking a guess')
            print(sudo)
            break
    return sudo

def solve(sudo):

    cell_dict, sudo = simple_solver(sudo)
    sudo = unique_poss_solver(cell_dict,sudo)
    cell_dict, sudo = simple_solver(sudo)
    sudo = unique_poss_solver(cell_dict,sudo)
    
    return sudo