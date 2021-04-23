"""
TubeCNC G-Code Generator

This is a class to generate G-Code for a custom 3-axis tube-cutting CNC designed by NUAV.
The current version (4/21/21) is capable of generating G-Code for hole drilling of square cross-section tubes

To do:
-Implement circular cross section csv file format

Basic use:
-Run gcodeGen.py in the same working directory as a .csv file
-Type inputs as they appear in the terminal
-Upload output file to Duet

Contributors:
- Noah Ossanna
- Michael Tang
- Alyssa Mui
"""

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

class Gcodegen:
    def __init__(self):
        #Define attributes as static parameters for export tuning (default units: mm)

        self.y_index_rate = 1000                                                                #set speed of y-plunge when indexing a hole position to avoid "walking"
        self.y_index_depth = 0.5                                                                #set depth of hole index before the bit backs out and performs the drill plunge
        self.y_index_retract = self.y_index_depth + 0.2                                         #set retraction after y-plunge before drill plunging
        self.y_dry_height = 3                                                                   #height above the stock to jog to during dry-run operations
        self.y_clearance_height  = 5                                                            #set some arbitrary clearance increment for y-retracts to be offset above features that we want to avoids
        self.z_chuck_clearance = 66                                                             #minimum measured horizontal clearance from the center of the chuck to a non-interfering plunge position of the router
        self.chuck_height = 70                                                                  #Height of the chuck measured from the center axis of rotation of the stock
       
        #Define movement rates
        self.x_move_rate = 200
        self.y_drill_rate = 50                                                                  #Plunge rate of the actual drilling operation
        self.z_move_rate = 500
        self.y_retract_rate = 85
        self.y_move_rate = 100

        #Default inputs (overrrdden by inputvar() method below)
        self.file_name = 'test.csv'       
        self.cross_section = 'square'    
        self.operation_type = 'dry run' 
        self.output_file_name = 'holes.gcode'
        self.stock_diam = 28.7             
        self.stock_length = 100        
        self.chuck_data = '200,800'     
        self.drill_depth = 4              
        self.y_chuck_retract = self.chuck_height - self.stock_diam/2 + self.y_clearance_height  #calculate y-retraction dynamically as a function of cross section

    def inputvar(self):
        #create user input variables

        #Stock type
        print('\nEnter the cross section type: Enter 0 for \'square\' and 1 for \'circle\'')
        choice_0 = 0
        choice_0 = input()
        if (choice_0 == '0'):
            self.cross_section = 'square'
        else:
            self.cross_section = 'circle'
        print('Cross section: ' + self.cross_section)

        #Operation type
        print('\nEnter the operation type: Enter 0 for \'dry-run\' and 1 for \'cut\'')
        choice_1 = 0
        choice_1 = input()
        if (choice_1 == '0'):
            self.operation_type = 'dry run'
        else:
            self.operation_type = 'cut'
        print('Operation type: ' + self.operation_type)

        #Stock cross section dimensions
        if (self.cross_section == 'square' ):
            print('\nEnter square flat-to-flat distance (mm): ')
        else:
            print('\nEnter outer diameter (mm): ')
        self.stock_diam = input()
        print('Stock diameter: ' + self.stock_diam)

        #stock length
        print('\nEnter the stock length (mm): ')
        self.stock_length = input()
        print('Stock Length: ' + self.stock_length)

        #chuck positions
        print('\nEnter the chuck positions separated by commas (absolute from origin in mm) : 1,2 ')
        self.chuck_data = input()
        print('Chuck positions: ' + self.chuck_data)

        #drill depth
        print('\nEnter the drill depth (mm): ')
        self.drill_depth = input()
        print('Drill depth: ' + self.drill_depth)

    def error_checker(self):
        """
        check if any input hole positions:
        - interfere with chuck positions
        - extend beyond stock lenth
        If so: output error (DOES NOT STOP GCODE GEN)
        """

        hole_data = pd.read_csv(self.file_name)   
        hole_pos = np.array(hole_data)        
        chuck_pos = self.chuck_data.split(',')                                      #transofrm chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = int(chuck_pos[i])
        
        
        num_rows = len(hole_pos[:,1])
        num_columns = len(hole_pos[1,:])
        avoid_threshold = self.y_clearance_height + self.z_chuck_clearance
        length = int(self.stock_length)

        for i in range(num_rows):  
            if abs(hole_pos[i,0] - chuck_pos[0]) < avoid_threshold:
                # print(abs(hole_pos[i,0] - chuck_pos[0]))
                print('\nWARNING: Cut paths intersect with chuck {} position at z = {}! Move chucks before cutting!'.format(1,hole_pos[i,0]))
            elif  abs(hole_pos[i,1] - chuck_pos[1]) < avoid_threshold:
                # print(abs(hole_pos[i,0] - chuck_pos[1]))
                print('\nWARNING: Cut paths intersect with chuck {} position at z = {}! Move chucks before cutting!'.format(2,hole_pos[i,0]))
            elif hole_pos[i,0] > length:
                print('\nWARNING: Cut paths at z = {} extend beyond stock length! Check input file.'.format(hole_pos[i,0]))
            else:
                print()

    def y_index(self):
        # index y-operations

        g.feed(self.y_move_rate)
        g.abs_move(y=self.y_clearance_height)
        g.feed(self.y_index_rate)
        g.abs_move(y=-self.y_index_depth)
        g.feed(self.y_retract_rate)
        g.abs_move(y=self.y_index_retract)

    def y_drill(self):
        #plunge y operations
        drill_depth = int(self.drill_depth)                                             #convert drill_depth input to int

        g.feed(self.y_retract_rate)
        g.abs_move(y=self.y_index_retract)
        g.feed(self.y_drill_rate)
        g.abs_move(y=-drill_depth)
        g.abs_move(y=self.chuck_height + self.y_clearance_height)                       #Critical: retract to clearance height above chucks before next z move to avoid collisions
        
    def y_dry(self):
        #dry-run y operations

        g.feed(self.y_move_rate)
        g.abs_move(y=self.y_dry_height)
        g.abs_move(y=self.chuck_height + self.y_clearance_height) 

    def y_operations(self):
        """
        Control y G-Code generation:
        - for 'cut' operations, execute cutting methods
        - for 'dry-run' operations, jog to hole position but do not plunge 
        """
        if self.operation_type == 'cut':
            self.y_index()
            self.y_drill()
        else:
            self.y_dry()

    def codeGen(self):
        #Generate G-Code

        hole_data = pd.read_csv(self.file_name)                                     #read input csv file (must be in same directory as script)
        hole_pos = np.array(hole_data)                                              #append csv to array format  
        stock_diam = int(self.stock_diam)                                           #convert stock_diam input to int        

        chuck_pos = self.chuck_data.split(',')                                      #transofrm chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = int(chuck_pos[i])
    

        num_rows = len(hole_pos[:,1])
        num_columns = len(hole_pos[1,:])
        y_index_depth = self.y_index_depth
        z_move_rate = self.z_move_rate
        y_move_rate = self.y_move_rate
        x_move_rate = self.x_move_rate
        self.error_checker()

        for i in range(num_rows):
            for j in range(num_columns):
        
                if hole_pos[i,j] == 666:                                            #do not generate G-code for unwanted angles
                    continue
                elif i == 0 and j == 0:
                    # print(i)
                    # print(j)                       
                    g.feed(z_move_rate)
                    g.abs_move(z=hole_pos[i,0])    
                elif i != 0 and j == 0:
                    rel_pos = np.subtract(hole_pos[i,0],hole_pos[0,0])
                    g.feed(z_move_rate)
                    g.move(z=rel_pos)      
                else:                         
                    if hole_pos[i,j] == 0:    
                        g.feed(y_move_rate)
                        g.abs_move(y=stock_diam)
                        self.y_operations()
                        
                    else:                 
                        g.feed(y_move_rate)
                        g.abs_move(y=stock_diam)             
                        g.feed(x_move_rate)
                        g.abs_move(x=hole_pos[i,j])  
                        self.y_operations()
        
script_directory = os.path.dirname(os.path.abspath(__file__))                        #Find the users working directory
output_directory = os.path.join(script_directory,'holes.gcode')                      #Append file name to working directory path
g = G(outfile = output_directory)                                                    #Instantiate MeCode object

# g.move(z=0)

test = Gcodegen()                                                                    
test.inputvar()                                                                     #run dynamic user inputs
test.codeGen()    
print('\nYour G-Code has been generated here: \n{}'.format(output_directory))  


        


