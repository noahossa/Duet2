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
        self.y_index_rate = 25                                                                #set speed of y-plunge when indexing a hole position to avoid "walking"
        self.y_index_depth = 0.5                                                                #set depth of hole index before the bit backs out and performs the drill plunge
        self.y_index_retract = self.y_index_depth + 0.2                                         #set retraction after y-plunge before drill plunging
        self.y_dry_height = 3                                                                   #height above the stock to jog to during dry-run operations
        self.y_clearance_height  = 5                                                            #set some arbitrary clearance increment for y-retracts to be offset above features that we want to avoids
        self.z_chuck_clearance = 66                                                             #minimum measured horizontal clearance from the center of the chuck to a non-interfering plunge position of the router
        self.chuck_height = 70                                                                  #Height of the chuck measured from the center axis of rotation of the stock
       
        # Define movement rates
        self.x_move_rate = 2000
        self.y_drill_rate = 40                                                                  #Plunge rate of the actual drilling operation
        self.z_move_rate = 2500
        self.y_retract_rate = 150
        self.y_move_rate = 350

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

        chuck_pos = self.chuck_data.split(',')                                      #transform chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = float(chuck_pos[i])
        
        num_rows = len(hole_pos[:,1])
        num_columns = len(hole_pos[1,:])
        avoid_threshold = self.y_clearance_height + self.z_chuck_clearance
        length = float(self.stock_length)

        for i in range(num_rows):  
            for j in range(len(chuck_pos)):
                if abs(hole_pos[i,0] - chuck_pos[j]) < avoid_threshold:
                    # print(abs(hole_pos[i,0] - chuck_pos[0]))
                    print('\nWARNING: Cut paths intersect with chuck {} position at z = {}! Move chucks before cutting!'.format(j+1,hole_pos[i,0]))

            if hole_pos[i,0] > length:
                print('\nWARNING: Cut paths at z = {} extend beyond stock length! Check input file.'.format(hole_pos[i,0]))
            else:
                print()
        print("- - - Check Complete - - ")


    def z_chuck_pos_check(self, row_index=None, first=False):
        """
        Checks for the position of the chucks and sees if it is between two z positions. Then it dynamically adjusts the y height based on if a chuck is present between the two z positions or not.
        - it should be called before any z axis movements
        - avoid striking any chucks
        """
        hole_data = pd.read_csv(self.file_name)   
        hole_pos = np.array(hole_data)

        chuck_pos = self.chuck_data.split(',')                                      #transform chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = float(chuck_pos[i])

        num_rows = len(hole_pos[:,1])
        avoid_threshold = self.y_clearance_height + self.z_chuck_clearance

        holes_left = abs(len(range(row_index+1)) - num_rows)                        #Establishes the number holes left that must be generated.

        if holes_left == 0 or first == True:                                                         #Checks for the last hole condition to ensure there isn't any indexing error if it tries to compare to future hole
            self.feed(self.y_move_rate)
            self.abs_move(y=float(self.stock_diam))
        else:
            for i in range(len(chuck_pos)):
                chuck_z_length_upper_bound = chuck_pos[i] + avoid_threshold/2
                chuck_z_length_lower_bound = chuck_pos[i] - avoid_threshold/2
                if hole_pos[row_index,0] < chuck_z_length_lower_bound and hole_pos[row_index+1,0] > chuck_z_length_upper_bound:             #Checks if the first hole's z position is less than the z position of the closest side of the chuck and checks if the second hole's z position is greater than the far side of the chuck
                    self.feed(self.y_retract_rate)
                    self.abs_move(y=self.chuck_height + self.y_clearance_height)
                    break
                else:                                                               #If the drill bit does not travel over a chuck just move at stock diameter y height
                    self.feed(self.y_move_rate)
                    self.abs_move(y=float(self.stock_diam))


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
        drill_depth = float(self.drill_depth)                                             #convert drill_depth input to int

        self.feed(self.y_retract_rate)
        self.abs_move(y=self.y_index_retract)
        self.feed(self.y_drill_rate)
        self.abs_move(y=-drill_depth)
        
    def y_dry(self):
        #dry-run y operations

        self.feed(self.y_move_rate)
        self.abs_move(y=self.y_dry_height)
        self.dwell(10000)

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

    #TODO: This is kinda of a bandaid for a bigger problem. Only to be used for debug purposes if motors start overheating
    def set_power(self, x_pow=100, y_pow=100, z_pow=100):                           
        '''
        Method to set the percentage of the power limit for each axis
        :param x_pow: int for the x power percentage (ex: 100, 50)
        :param y_pow: int for the y power percentage
        :param z_pow: int for the z power percentage
        '''
        self.write('M913 X{} Y{} Z{};'.format(x_pow, y_pow, z_pow))

    def y_retract(self):
        self.feed(self.y_move_rate)
        self.abs_move(y=self.chuck_height + self.y_clearance_height)

    def codeGen(self):
        #Generate G-Code

        hole_data = pd.read_csv(self.file_name)                                     #read input csv file (must be in same directory as script)
        hole_pos = np.array(hole_data)                                              #append csv to array format  
        stock_diam = float(self.stock_diam)                                           #convert stock_diam input to int        

        chuck_pos = self.chuck_data.split(',')                                      #transform chuck_pos from input as a list to an array
        for i in range(0, len(chuck_pos)):                                          #convert chuck string input to array of ints
            chuck_pos[i] = float(chuck_pos[i])
    
        num_rows = len(hole_pos[:,1])
        num_columns = len(hole_pos[1,:])
        y_index_depth = self.y_index_depth
        z_move_rate = self.z_move_rate
        y_move_rate = self.y_move_rate
        x_move_rate = self.x_move_rate
        self.error_checker()

        self.z_chuck_pos_check(row_index=0, first=True)
        #self.y_retract()                                                            #Critical: retract to clearance height above chucks before any z move to avoid collisions
        for i in range(num_rows):
            for j in range(num_columns):
        
                if hole_pos[i,j] == 666:                                            #do not generate G-code for unwanted angles
                    continue
                elif i == 0 and j == 0:                      
                    self.feed(z_move_rate)
                    self.abs_move(z=hole_pos[i,0])    
                elif i != 0 and j == 0:
                    rel_pos = hole_pos[i,0]
                    self.feed(z_move_rate)
                    self.abs_move(z=rel_pos)      
                else:                         
                    if hole_pos[i,j] == 0:    
                        self.feed(y_move_rate)
                        self.abs_move(y=stock_diam)
                        self.y_operations()
                        self.z_chuck_pos_check(row_index=i)
                        
                    else:                 
                        self.feed(y_move_rate)
                        self.abs_move(y=stock_diam)  

                        self.set_power(x_pow=100)           
                        self.feed(x_move_rate)
                        self.abs_move(x=hole_pos[i,j])  
                        self.set_power(x_pow=40)  
                        self.y_operations()
                        self.z_chuck_pos_check(row_index=i)
        
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
    output_directory = os.path.join(script_directory,options.output_file)                      #Append file name to working directory path

    g = G(outfile = output_directory) #Instantiate MeCode object
    
    test = Gcodegen(options, outfile = output_directory)                                                                    
    # test.inputvar()                                                                     #run dynamic user inputs
    test.codeGen()    
    print('\nYour G-Code has been generated here: \n{}'.format(output_directory))  

if __name__ == '__main__':
    main()

