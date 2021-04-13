# Duet2
Repository for custom Duet configuration files and scripts

![CNC-axis](<blockquote class="imgur-embed-pub" lang="en" data-id="a/rnS9JUQ"  ><a href="//imgur.com/a/rnS9JUQ">Tube_CNC_Axis</a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>)
## Workflow
* Make csv file
* apply function args
* export gcode to clipboard and past in text doc, save as gcode file and upload to [Duet Web Control (DWC)](https://duet3d.dozuki.com/Wiki/Duet_Web_Control_Manual), jobs tab
* export dry run gcode and test
* export drill run of gcode and run
### Inputs
* will we have a UI? 
* cross section shape
* cross section dia or flat-to-flat
* Assume origin at 12 o'clock pos end of stock (printout of this as a warning assumption?)
    *  USE DISCRETION for square stock to place origin on face such that X-axis rotation is limited
* Length of stock
* chuck positions 
* specify drill or dry-run gcode export? (do everything but the Y-plunge), go to all holes and touch surface (marker bit in cnc)
* plunge depth 
* all exclusions (Y and for chucks) will be set based on lower level function params (can make these inputs later but not priority)

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
[G code Dictionary](https://duet3d.dozuki.com/Wiki/Gcode#Section_G_Code_Structure)
[Calculators for belts for Stepper Motors](https://blog.prusaprinters.org/calculator_3416/)
[CSV Docs](https://docs.python.org/3/library/csv.html)
[CSV Use](https://stackoverflow.com/questions/57406217/how-to-pass-csv-file-as-an-argument-to-python-file)
