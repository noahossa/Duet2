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

#Define parameters to choose from (eventually make these class attributes)
#------------------------------------------------------------------------------------------------------------------------
cross_section_types = ['square','circle']    #should implement function get_cross_section() to determine section based on user input
operation_types = ['sim', 'real']            #define sim and real parameters to choose between oyutputting "dry" drilling operations (without plunges for simulation) and actual operations (with plunges for cutting) respectively
num_chucks = 2 #default number of chucks
chuck_height = 70                         #need to fix this to be whatever height the chuck is above the CENTER of the stock (will perform y-hop calcs based on stock dia to keep this number as a fixed, low-level parameter)

#Set STATIC params that the user (or developer) shouldnt change a lot after initial tuning (LITERALLY pulling these numbers out of my ass rn, we need to test these)
y_index_rate = 1000         #set some value for the speed of y-plunge when indexing a hole position to avoid "walking"
y_index_depth = 0.5         #set depth of hole index plunge before the bit backs out and drills the acrual hole at speed
y_index_retract = y_index_depth + 0.2 #set retraction after y-plunge before actual drilling operation

#Define movement rates
x_move_rate = 200
y_drill_rate = 50          #set rate of actual drilling operation
z_move_rate = 500
y_retract_rate = 85
y_move_rate = 100

clearance_distance  = 5      #set some arbitrary clearance increment for y-retracts to be offset above features that we want to avoids
#------------------------------------------------------------------------------------------------------------------------

#Statis define user input variables (default units = mm)
#-----------------------------------------------------------------------------------------------------------------------
file_name = 'test.csv'       #to be replaced by below input (this is the name of the input gcode file)
cross_section = 'square'      #to be replaced by below input (this is the cross section of the stock)
stock_diam = 28.7             #replace with "None" to work with below dynamic inputs (this is either the circular diameter or flat to flat measurement of the stock)
stock_length = 1000           #to be replaced by below input (this is the length of the stock for setting end points in the gcode? this might not be necessary)
chuck_pos = [200, 800]        # to be replaced by "[]" and be populated by below for loop input (this is an array of chuck positions measured absolute from the edge of the stock)
drill_depth = 4               # to be replaced by below input (this is the depth to drill on each face)

#Dynamic user inputs (uncomment after replacing static)

# file_name = input("filename:")          #allows user to input a filename to pull the csv from. Have to be careful at what level the working directory is located currently, as users have to prepend the file path from the terminal to their file name
# cross_section = input("cross section type:")

# if cross_section == 'square':                                            #dynamically adjust user input string depending on cross section
#     diam_input_string = 'Enter square flat-to-flat distance (mm):' 
#     else:
#          diam_input_string = 'Enter outer diameter (mm):'   
# stock_diam = input(diam_input_string)

# stock_length = input('Enter length of stock')

# for i in num_chucks:                                                                 #dynamically build array of chuck positions
#     chuck_input_string = 'Enter absolute distance of chuck {} (mm):'.format(i)
#     chuck_pos[i] = input(chuck_input_string)

#drill_depth = input('Enter depth to drill (mm):'


#Set Dynamic Params based on user inputs and STATIC params
#-----------------------------------------------------------------------------------------------------------------------------------------
hole_data = pd.read_csv(file_name)      #reads file at the work directory level aka the level the terminal is being run at
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
#------------------------------------------------------------------------------------------------------

#Pre-generation calculations based on user inputs and static params
#------------------------------------------------------------------------------------------------------
y_chuck_retract = chuck_height - stock_diam/2 + clearance_distance

def y_index():
    g.feed(y_move_rate)
    g.abs_move(y=1)
    g.feed(y_index_rate)
    g.abs_move(y=-y_index_depth)
    g.feed(y_retract_rate)
    g.abs_move(y=y_index_retract)

def y_drill():
    g.feed(y_retract_rate)
    g.abs_move(y=y_index_retract)
    g.feed(y_drill_rate)
    g.abs_move(y=-drill_depth)
#------------------------------------------------------------------------------------------------------

#generate g-code in enxted for loop
#------------------------------------------------------------------------------------------------------
for i in range(num_rows):
    for j in range(num_columns):
 
        if hole_pos[i,j] == 666:  #if any of the column entries in a row of hole_pos are strings, then do not generate gcode (no holes are located here)
            continue
            
        #generate z-coordinate gcode (accompanying y retracts?)
        elif i == 0 and j == 0:                        #if we are at the first column of a row, we know that this is a ABSOLUTE z-coordinate location
            g.feed(z_move_rate)
            g.abs_move(z=hole_pos[i,0])    #Sends an absolute move command in the z-axis regardless of rotation
        elif i != 0 and j == 0:
            rel_pos = np.subtract(hole_pos[i,0],hole_pos[0,0]) #subtracts the current position from the first postion to establish a relative position to be used in the g.move command
            g.feed(z_move_rate)
            g.move(z=rel_pos)       #sends a relative move command in the z-axis regardless of rotation
        else:                                #else if the loop hasn't exited at this point, there must be a rotation, which should be accomplished followed by a drill operation
            if hole_pos[i,j] == 0:      #if the first z-coordinate is zero, then we dont need to move anywhere and can drill immediatly!
                g.feed(y_move_rate)
                g.abs_move(y=5)
                y_index()
                y_drill()
            else:                   #need to rotate if there must a hole drilled at a different rotational position other than its current position
                g.feed(y_move_rate)
                g.abs_move(y=5)                #y-axis is raised to avoid striking the member
                g.feed(x_move_rate)
                print(hole_pos[i,j])
                g.abs_move(x=hole_pos[i,j])     #if the loop hasn't exited yet at this point, then at the column position of the given row, there must a drill point
                y_index()
                y_drill() 
#------------------------------------------------------------------------------------------------------





