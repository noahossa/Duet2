G90 ; use absolute coordinates
M83 ; extruder relative move

G28 YZ; Home Y and Z axis using Sensorless homing

G4 S10; Pause the machine to allow for manual manipulation of the tool to center it

G1 Y20 F5000; Set y-axis to move up to 20mm pos
G1 Z50 F5000; Set z-axis to move to the 50mm pos
G1 Y0 F2000; Set y-axis to move down to 0mm pos

G1 Y20 F5000;
G28 Z; Go to z-axis home