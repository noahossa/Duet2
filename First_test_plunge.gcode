G90 ; use absolute coordinates
M83 ; extruder relative move

G1 Y47 F5000; Set y-axis to move up to 20mm pos
G1 Z50 F5000; Set z-axis to move to the 50mm pos

G4 S3;

G1 Y0 F2000; Set y-axis to move down to 0mm pos
G1 Y40 F5000;
