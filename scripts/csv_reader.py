import csv
import argparse

with open('test.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    print(spamreader)
    for row in spamreader:
        print(', '.join(row))