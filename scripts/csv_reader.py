#!/usr/bin/env python
import csv
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyperclip as pc
import mecode
from mecode import G
import pathlib
import os


# file_name = input("filename:")          #allows user to input a filename to pull the csv from. Have to be careful at what level the working directory is located currently, as users have to prepend the file path from the terminal to their file name
hole_data = pd.read_csv('test.csv')      #reads file at the work directory level aka the level the terminal is being run at
# hole_data = pd.read_csv(file_name)
hole_pos = np.array(hole_data)          #append csv to remove column labels
# print(hole_pos)

num_rows = len(hole_pos[:,1])
num_columns = len(hole_pos[1,:])

#instantiate the gcode object g
#output constructed to a file in our repo
script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(script_directory, 'holes.gcode') #already a string
g = G(outfile = output_directory)

#add common gcode commands that need to be at the beginning of all files
    #g.home()

#generate g-code in enxted for loop
for i in range(num_rows - 1):
    for j in range(num_columns - 1):

        if hole_pos[i,j] == 'E':  #if any of the column entries in a row of hole_pos are strings, then do not generate gcode (no holes are located here)
            continue
            
        #generate z-coordinate gcode (accompanying y retracts?)
        elif i == 0 and j == 0:                        #if we are at the first column of a row, we know that this is a ABSOLUTE z-coordinate location
            g.abs_move(z=hole_pos[i,0])    #Sends an absolute move command in the z-axis regardless of rotation
        elif i != 0 and j == 0:
            rel_pos = np.subtract(hole_pos[i,0],hole_pos[0,0]) #subtracts the current position from the first postion to establish a relative position to be used in the g.move command
            g.move(z=rel_pos)       #sends a relative move command in the z-axis regardless of rotation
        else:                                #else if the loop hasn't exited at this point, there must be a rotation, which should be accomplished followed by a drill operation
            if hole_pos[i,j] == 0:      #if the first z-coordinate is zero, then we dont need to move anywhere and can drill immediatly!
                g.abs_move(y=20)#DRILL COMMAND must be placed here!!!
            else:                   #need to rotate if there must a hole drilled at a different rotational position other than its current position
                g.abs_move(y=20)                #y-axis is raised to avoid striking the member
                g.abs_move(x=hole_pos[i,j])     #if the loop hasn't exited yet at this point, then at the column position of the given row, there must a drill point 
            #DRILL COMMANDS must be placed here!!!






