# Duet2
Repository for custom Duet configuration files and scripts

<a href="https://ibb.co/68RzfXk"><img src="https://i.ibb.co/68RzfXk/LdKgD7n.png" alt="LdKgD7n" border="0"></a>

## Workflow
* Make csv file
    * Important Note: When creating a csv file, ensure that it is only CSV (Comma Delimited) as other encoding formats prepend data on the front of data
* apply function args
* export gcode to clipboard and past in text doc, save as gcode file and upload to [Duet Web Control (DWC)](https://duet3d.dozuki.com/Wiki/Duet_Web_Control_Manual), jobs tab
* export dry run gcode and test
* export drill run of gcode and run
### To-dos
* Find better method for excluding holes than 666
* Look at ways to add comments into exported gcode using mecode (make it more readible)
* Need to implement logic to avoid chucks (need param to input chuck width)
* Clean up comments and update readme
* Better picture of tube CNC axes
* Add auxillary functions like relay control


* CSV: array of Z positions for hole "sets" AND X positions for each hole in that set (with respect to the chosen origin)
    * Z5.351, X90, X-90 
    * Z10, X90, 0 (zero means no other holes)
        * arrays would be dimensioned with columns equal to Z-position with max number of holes

### Method
* Make first hole "index" the rest, gcode using absolute coordinates to the first hole, all relative after to avoid stacks
* Absolute coordinates for first hole, then all holes on same Z-position drilled using X and Y motions ONLY
* After all holes on a given Z-position are drilled, advance to the next using relative position indexing, then repeat relative X and Y motions until all holes are drilled at that Z-position
* based on cross section shape and dia, chuck positions, and stock length, script will generate correct y-retracts to avoid collisions
    * param could be "z-chuck exclusion offset" 

## Scripts
Python scripts and examples for generating GCode according to
[Mecode](https://reprap.org/wiki/Mecode#Matrix_Transforms)


## References
* [G code Dictionary](https://duet3d.dozuki.com/Wiki/Gcode#Section_G_Code_Structure)
* [Calculators for belts for Stepper Motors](https://blog.prusaprinters.org/calculator_3416/)
* [CSV Docs](https://docs.python.org/3/library/csv.html)
* [CSV Use](https://stackoverflow.com/questions/57406217/how-to-pass-csv-file-as-an-argument-to-python-file)
* [argparse](https://prod.liveshare.vsengsaas.visualstudio.com/join?6DCFD36A06689E096F402D0AF10C7EC8E8DD)

## Steps

Install [pandas](https://pandas.pydata.org/)
```bash
pip install pandas
```

Install [numpy/matplotlib](https://numpy.org/install/) and reference [tutorial](https://realpython.com/numpy-tutorial/)
``` bash
pip install numpy matplotlib
```

Install [mecode](https://reprap.org/wiki/Mecode)
``` bash
pip install mecode
```