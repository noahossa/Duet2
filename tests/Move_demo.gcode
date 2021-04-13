G90 ; use absolute coordinates
M83 ; extruder relative move

G1 Y20 F5000; Set y-axis to move up to 20mm pos

G4 S3;

G1 Z150 X180 F1000; Set y-axis to move down to 0mm pos
G1 Y8 F7500;

G1 Z125 F1000;

G1 Y1 F1000;
G1 Y8 F7500;