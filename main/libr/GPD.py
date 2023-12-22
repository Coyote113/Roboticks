'''
Cole Johnson 11/20/23

gps point data or GPD method and class.

gpd stands for gps point data.
the gpd array is the array of gps points we want to hit with the robots movement

this file creates a gpd object with is used to interact with the path.txt data file.

in general it converts the txt file into an array inside the gpd object, which can then be moved through
using functions in the gpd object.

the gpd object can also be used to write data to the path.txt file by calling its write function.
'''

import math

import libr.framework as fw


class create_GPD:
    def __init__(self, FN, auto_read_txt = False):
        self.FN = FN # saves the file name
        self.gpd_array = [] # creates an empty array for the pata points to be added to
        self.index = 0 # creates an index value

        if auto_read_txt == True: # reads from the file when the class is created instead of being delayed
            self.read_txt_to_arr()


    # reads the text file and puts in in an array
    # returns the completed array but that should not be the main use of this method
    def read_txt_to_arr(self):
        self.gpd_array.clear() # clear the current gpd array
        f = open(self.FN, 'r') # open the file in read mode
        for line in f.readlines(): # read lines in file
            l = line.split(', ') # split the str at the comma into 2 points
            self.gpd_array.append((float(l[0]), float(l[1]))) 
            # convert the str to a float and append the point to the gpd array
        f.close()
        return self.gpd_array
    

    # returns the array without having to reopen the txt file
    # should be used instead of the function above when trying to get the gpd array
    def get_full_gpd_arr(self):
        return self.gpd_array


    # returns a bool based of if there is anything in the array
    def gpd_exists(self):
        if self.gpd_array == [] or self.gpd_array == None: return False
        return True # if above is not true return true


    # writes an array of points to the txt file in the correct format
    def write_arr_to_txt(self, arr):
        arr_str = [] # creates empty array to be in txt format
        for point in arr: # for each point in the passed array
            #s = str(point[0]) + ', ' + str(point[1]) + '\n' # convert to txt format
            s = str(point[0]) + ', ' + str(point[1])
            arr_str.append(s) # append to the new array
            print('append ' + str(s))
        f = open(self.FN, 'w') # open file in write mode
        for line in arr_str: # for each point in the arr
            f.write(line) # write the str point to the current line
            print('write ' + str(line))
            f.write('\n') # skip to the next line
        f.close()


    # gets the current point as an str
    # useful for debug but not much else
    def get_current_point_in_arr_str(self):
        return self.gpd_array[self.index]
    
    # gets the current points (x and y) lon and lat values in tuple format (lon, lat)
    def get_current_point_in_arr_float(self):
        lon = float(self.gpd_array[self.index][0])
        lat = float(self.gpd_array[self.index][1])
        return (lon, lat)
    
    # gets the current points lon (x) value
    def get_current_point_in_arr_float_lon(self):
        lon = float(self.gpd_array[self.index][0])
        return (lon)
    
    # gets the current points lat (y) value
    def get_current_point_in_arr_float_lat(self):
        lat = float(self.gpd_array[self.index][1])
        return (lat)
    

    # jumps the index of the gpd array forward or backward by a specific amount
    # jump is +1 by default by default
    def jump_idx(self, jump = 1):
        self.index += jump
        # upper bound check
        if self.index >= len(self.gpd_array):
            self.index = len(self.gpd_array) - 1
        # lower bound check
        if self.index < 0:
            self.index = 0

    # resets the index to the start of the array
    def reset_idx(self):
        self.index = 0
    
    # gets the current index
    def get_idx(self):
        return self.index


    # checks if the index is at the end of the gpd array
    def at_end_of_gpd_arr(self):
        if self.index == len(self.gpd_array) - 1:
            return True
        else: return False

    # checks if the index is at the start of the gpd array
    def at_start_of_gpd_arr(self):
        if self.index == 0:
            return True
        else: return False


    # gets the length of the gpd array
    def len_of_gpd_arr(self):
        return len(self.gpd_array)