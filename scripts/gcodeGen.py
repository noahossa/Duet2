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

        #Set STATIC params that the user (or developer) shouldnt change a lot after initial tuning (LITERALLY pulling these numbers out of my ass rn, we need to test these)
        self.y_index_rate = 1000         #set some value for the speed of y-plunge when indexing a hole position to avoid "walking"
        self.y_index_depth = 0.5         #set depth of hole index plunge before the bit backs out and drills the acrual hole at speed
        self.y_index_retract = self.y_index_depth + 0.2 #set retraction after y-plunge before actual drilling operation

        #Define movement rates
        self.x_move_rate = 200
        self.y_drill_rate = 50          #set rate of actual drilling operation
        self.z_move_rate = 500
        self.y_retract_rate = 85
        self.y_move_rate = 100

        self.clearance_distance  = 5      #set some arbitrary clearance increment for y-retracts to be offset above features that we want to avoids
        
        self.cross_section_types = ['square','circle']    #should implement function get_cross_section() to determine section based on user input
        self.operation_types = ['sim', 'real']            #define sim and real parameters to choose between oyutputting "dry" drilling operations (without plunges for simulation) and actual operations (with plunges for cutting) respectively
        self.num_chucks = 2 #default number of chucks
        self.chuck_height = 70                         #need to fix this to be whatever height the chuck is above the CENTER of the stock (will perform y-hop calcs based on stock dia to keep this number as a fixed, low-level parameter)

        #Set STATIC params that the user (or developer) shouldnt change a lot after initial tuning (LITERALLY pulling these numbers out of my ass rn, we need to test these)
        self.y_index_rate = 30         #set some value for the speed of y-plunge when indexing a hole position to avoid "walking"
        self.y_index_depth = 0.5         #set depth of hole index plunge before the bit backs out and drills the acrual hole at speed
        self.y_index_retract = self.y_index_depth + 0.2 #set retraction after y-plunge before actual drilling operation

        self.y_drill_rate = 5000          #set rate of actual drilling operation
        self.y_clearance_height  = 5      #set some arbitrary clearance increment for y-retracts to be offset above features that we want to avoids

        #Statis define user input variables (default units = mm)
        self.file_name = 'test.csv'       
        self.cross_section = 'square'     
        self.output_file_name = 'holes.gcode'
        self.stock_diam = 28.7             
        self.stock_length = 1000          
        self.chuck_pos = [200, 800]       
        self.drill_depth = 4              

        self.y_chuck_retract = self.chuck_height - self.stock_diam/2 + self.clearance_distance

        # self.script_directory = os.path.dirname(os.path.abspath(__file__))
        # self.output_directory = os.path.join(self.script_directory,self.output_file_name) 
        # g = G(outfile = self.output_directory)

    # Prompts the user to input all variables
    def inputvar(self):
        print('Enter the cross section type: Enter 0 for \'square\' and 1 for \'circle\'')
        choice = 0
        choice = input()
        if (choice == 0):
            self.cross_section = 'square'
        else:
            self.cross_section = 'circle'
            
        print('Cross section: ' + self.cross_section)

        if (self.cross_section == 'square' ): #dynamically adjust user input string depending on cross section
            print('Enter square flat-to-flat distance (mm): ')
        else:
            print('Enter outer diameter (mm): ')

        self.stock_diam = input()

        print('Stock diameter: ' + self.stock_diam)

        print('Enter the stock length (mm): ')
        self.stock_length = input()
        print('Stock Length: ' + self.stock_length)

        print('Enter the chuck position: [x,y]')
        self.chuck_pos = input()
        print('Stock Length: ' + self.stock_length)

        print('Enter the drill depth (mm): ')
        self.drill_depth = input()
        print('Drill depth: ' + self.drill_depth)
    
    def y_index(self):

        g.feed(self.y_move_rate)
        g.abs_move(y=1)
        g.feed(self.y_index_rate)
        g.abs_move(y=-self.y_index_depth)
        g.feed(self.y_retract_rate)
        g.abs_move(y=self.y_index_retract)

    def y_drill(self):

        g.feed(self.y_retract_rate)
        g.abs_move(y=self.y_index_retract)
        g.feed(self.y_drill_rate)
        g.abs_move(y=-self.drill_depth)
        
    def codeGen(self):
     
        # Read hole data
        hole_data = pd.read_csv(self.file_name)      #reads file at the work directory level aka the level the terminal is being run at
        # hole_data = pd.read_csv(file_name)
        hole_pos = np.array(hole_data)          #append csv to remove column labels
        # print(hole_pos)

        num_rows = len(hole_pos[:,1])
        num_columns = len(hole_pos[1,:])

        y_index_depth = self.y_index_depth
        z_move_rate = self.z_move_rate
        y_move_rate = self.y_move_rate
        x_move_rate = self.x_move_rate

        for i in range(num_rows):
            for j in range(num_columns):
        
                if hole_pos[i,j] == 666:  
                    continue
                elif i == 0 and j == 0:                       
                    g.feed(z_move_rate)
                    g.abs_move(z=hole_pos[i,0])    
                elif i != 0 and j == 0:
                    rel_pos = np.subtract(hole_pos[i,0],hole_pos[0,0])
                    g.feed(z_move_rate)
                    g.move(z=rel_pos)      
                else:                           
                    if hole_pos[i,j] == 0:    
                        g.feed(y_move_rate)
                        g.abs_move(y=self.stock_diam)
                        self.y_index()
                        self.y_drill()
                    else:                 
                        g.feed(y_move_rate)
                        g.abs_move(y=self.stock_diam)             
                        g.feed(x_move_rate)
                        g.abs_move(x=hole_pos[i,j])  
                        self.y_index()
                        self.y_drill() 
        
script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(script_directory,'holes.gcode') 
g = G(outfile = output_directory)

test = Gcodegen()
# test.inputvar()
test.codeGen()
print('Your code has been generated in:')
print(output_directory)

        


