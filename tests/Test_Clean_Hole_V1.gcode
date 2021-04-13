G90 ; use absolute coordinates
M83 ; extruder relative move

G1 Y20 F5000; Set y-axis to move up to 20mm pos

G4 S3;

G1 Y0 F3000; Set y-axis to move down to 0mm pos
G1 Y8 F7500;

G1 Y-1.5 F5000;
G1 Y8 F8500;

G1 Y-3 F5000;
G1 Y8 F9500;

G1 Y-4.5 F5000;
G1 Y8 F10500;

G1 Y-6 F5000;
G1 Y8 F10500;
