"""
TubeCNC G-Code Generator

This is a class to generate G-Code for a custom 3-axis tube-cutting CNC designed by NUAV.
The current version (5/22/21) is capable of generating G-Code for hole drilling of square cross-section tubes

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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mecode
from mecode import G
import pathlib
import os
from argparse import ArgumentParser

class Gcodegen(G):
    def __init__(self, options, **kwargs):
        super().__init__(**kwargs)

        '''
        :param options: argument inputs, see arguement_parser
        '''
        #Define attributes as static parameters for export tuning (default units: mm)
        self.y_index_rate = 1000                                                                #set speed of y-plunge when indexing a hole position to avoid "walking"
        self.y_index_depth = 0.5                                                                #set depth of hole index before the bit backs out and performs the drill plunge
        self.y_index_retract = self.y_index_depth + 0.2                                         #set retraction after y-plunge before drill plunging
        self.y_dry_height = 3                                                                   #height above the stock to jog to during dry-run operations
        self.y_clearance_height  = 5                                                            #set some arbitrary clearance increment for y-retracts to be offset above features that we want to avoids
        self.z_chuck_clearance = 66                                                             #minimum measured horizontal clearance from the center of the chuck to a non-interfering plunge position of the router
        self.chuck_height = 70                                                                  #Height of the chuck measured from the center axis of rotation of the stock
       
        # Define movement rates
        self.x_move_rate = 200
        self.y_drill_rate = 50                                                                  #Plunge rate of the actual drilling operation
        self.z_move_rate = 500
        self.y_retract_rate = 85
        self.y_move_rate = 100

        # Input Args
        self.file_name = str(options.input_file)  
        self.cross_section = str(options.cross_section)
        self.operation_type = str(options.operation_type)
        self.output_file_name = str(options.output_file)
        self.stock_diam = float(options.stock_diam)       
        self.stock_length = float(options.stock_len)     
        self.chuck_data = str(options.chuck_pos)   
        self.drill_depth = float(options.drill_depth)       

        # Calulated Vals
        self.y_chuck_retract = self.chuck_height - self.stock_diam/2 + self.y_clearance_height  #calculate y-retraction dynamically as a function of cross section

    def error_checker(self):    
        """
        check if any input hole positions:
        - interfere with chuck positions
        - extend beyond stock lenth
        If so: output error (DOES NOT STOP GCODE GEN)
        """
        print("- - - Checking Errors - - ")

        hole_data = pd.read_csv(self.file_name)   
        hole_pos = np.array(hole_data)        
        if " " in self.chuck_data:
            print("WARNING: SPACES IN CHUCK POSITIONS")
            exit(-1)

        chuck_pos = self.chuck_data.split(',')                                      #transofrm chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = float(chuck_pos[i])
        
        num_rows = len(hole_pos[:,1])
        num_columns = len(hole_pos[1,:])
        avoid_threshold = self.y_clearance_height + self.z_chuck_clearance
        length = float(self.stock_length)

        for i in range(num_rows):  
            for j in range(len(chuck_pos)):
                if abs(hole_pos[i,0] - chuck_pos[j]) < avoid_threshold:
                    print(f'\nWARNING: Cut paths intersect with chuck {j+1} position at z = {hole_pos[i,0]}! Move chucks before cutting!')

            if hole_pos[i,0] > length:
                print(f'\nWARNING: Cut paths at z = {hole_pos[i,0]} extend beyond stock length! Check input file.')
            else: 
                print()
        print("- - - Check Complete - - ")

    def y_index(self):
        # index y-operations

        self.feed(self.y_move_rate)
        self.abs_move(y=self.y_clearance_height)
        self.feed(self.y_index_rate)
        self.abs_move(y=-self.y_index_depth)
        self.feed(self.y_retract_rate)
        self.abs_move(y=self.y_index_retract)

    def y_drill(self):
        #plunge y operations
        drill_depth = float(self.drill_depth)                                              #convert drill_depth input to int

        self.feed(self.y_retract_rate)
        self.abs_move(y=self.y_index_retract)
        self.feed(self.y_drill_rate)
        self.abs_move(y=-drill_depth)
        self.abs_move(y=self.chuck_height + self.y_clearance_height)                       #Critical: retract to clearance height above chucks before next z move to avoid collisions
        
    def y_dry(self):
        #dry-run y operations

        self.feed(self.y_move_rate)
        self.abs_move(y=self.y_dry_height)
        self.abs_move(y=self.chuck_height + self.y_clearance_height) 

    def y_mark(self):
        #Draw a marker line at a given cut length
        self.feed(self.y_move_rate)
        self.abs_move(y=self.y_clearance_height)
        self.feed(self.y_index_rate)
        self.abs_move(y=0)
        self.abs_move(x=360)  


    def y_operations(self):
        """
        Control y G-Code generation:
        - for 'cut' operations, execute cutting methods
        - for 'dry-run' operations, jog to hole position but do not plunge 
        - for 'mark' operations, jog to hole position, stop at surface, then draw a line around the stock
        """
        if self.operation_type == 'cut':
            self.y_index()
            self.y_drill()
        elif self.operation_type == 'mark':
            self.y_mark()
        else:
            self.y_dry()

    def codeGen(self):
        #Generate G-Code

        hole_data = pd.read_csv(self.file_name)                                     #read input csv file (must be in same directory as script)
        hole_pos = np.array(hole_data)                                              #append csv to array format  
        stock_diam = float(self.stock_diam)                                           #convert stock_diam input to int        

        chuck_pos = self.chuck_data.split(',')                                      #transofrm chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = float(chuck_pos[i])
    

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
                    self.feed(z_move_rate)
                    self.abs_move(z=hole_pos[i,0])    
                elif i != 0 and j == 0:
                    rel_pos = np.subtract(hole_pos[i,0],hole_pos[0,0])
                    self.feed(z_move_rate)
                    self.move(z=rel_pos)      
                else:                         
                    if hole_pos[i,j] == 0:  
                        self.feed(y_move_rate)
                        self.abs_move(y=stock_diam)
                        self.y_operations()
                        
                    else:                 
                        self.feed(y_move_rate)
                        self.abs_move(y=stock_diam)             
                        self.feed(x_move_rate)
                        self.abs_move(x=hole_pos[i,j])  
                        self.y_operations()
        
def argument_parser():
    '''
    Method to parse the input args
    :return: options
    '''
    parser = ArgumentParser()
    parser.add_argument('--cross_section', type=str,choices=['square', 'circle'] ,default='square', help='tube cross section shape')
    parser.add_argument('--operation_type', type=str,choices=['cut', 'dry_run', 'print'] ,default='dry_run', help='operation type')
    parser.add_argument('--stock_diam', type=float, default=27.8, help='diameter of the stock (mm)')
    parser.add_argument('--stock_len', type=float, default=1775, help='length of the stock (mm)')
    parser.add_argument('--chuck_pos', type=str, default="400,700", help='chuck positions, must be inputted closest to farthest: comma separated (absolute from origin in mm). Ex: "240,480,..." ')
    parser.add_argument('--drill_depth', type=float, default=5, help='drilling depth from outer radius (mm)')

    parser.add_argument('--input_file', type=str, default='test.csv', help='hole drilling input file')
    parser.add_argument('--output_file', type=str, default='holes.gcode', help='output file name')
    
    return parser.parse_args()

def main():
    options = argument_parser()
    script_directory = os.path.dirname(os.path.abspath(__file__))                        #Find the users working directory
    output_directory = os.path.join(script_directory,'holes.gcode')                      #Append file name to working directory path
    
    test = Gcodegen(options, outfile = output_directory)                                                                    
    # test.inputvar()                                                                     #run dynamic user inputs
    test.codeGen()    
    print('\nYour G-Code has been generated here: \n{}'.format(output_directory))  

if __name__ == '__main__':
    main()

