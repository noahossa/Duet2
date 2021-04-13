import csv
import argparse
import pandas as pd

file_name = input("filename:") #allows user to input a filename to pull the csv from. Have to be careful at what level the working directory is located currently, as users have to prepend the file path from the terminal to their file name

df = pd.read_csv(file_name) #reads file at the work directory level aka the level the terminal is being run at
print(df)


# with open(file_name, newline='') as csvfile: #reads file at the work directory level aka the level the terminal is being run at
#     fileReader = csv.reader(csvfile)
#     for row in fileReader:
#         print(', ' .join(row))