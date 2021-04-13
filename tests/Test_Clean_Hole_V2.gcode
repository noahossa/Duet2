G90 ; use absolute coordinates
M83 ; extruder relative move

G1 Y10 F200; Set y-axis to move up to 20mm pos

G4 S3;

G1 Y0 F50; Set y-axis to move down to 0mm pos
G1 Y8 F150;

G1 Y0.5 F100;
G1 Y-1.5F50; Set y-axis to move down to 0mm pos
G1 Y8 F150;

G1 Y-1.0 F150
G1 Y-3 F50;
G1 Y8 F300;

G1 Y-2.5 F150
G1 Y-4.5 F50;
G1 Y8 F300;

G1 Y-4.0 F150
G1 Y-6 F50;
G1 Y8 F300;

G1 Y-5.5 F150
G1 Y-7.5 F50;
G1 Y8 F300;

G1 Y-7 F150
G1 Y-9 F50;
G1 Y8 F300;

G1 Y-8.5 F150
G1 Y-10.5 F50;
G1 Y8 F300;

G1 Y-10 F150
G1 Y-12.0 F50;
G1 Y8 F300;

G1 Y-11.5 F150
G1 Y-13.5 F50;
G1 Y20 F300;

G1 X90 F1000; rotation 90 degrees

G1 Y0 F50; Set y-axis to move down to 0mm pos
G1 Y8 F150;

G1 Y0.5 F100;
G1 Y-1.5F50; Set y-axis to move down to 0mm pos
G1 Y8 F150;

G1 Y-1.0 F150
G1 Y-3 F50;
G1 Y8 F300;

G1 Y-2.5 F150
G1 Y-4.5 F50;
G1 Y8 F300;

G1 Y-4.0 F150
G1 Y-6 F50;
G1 Y8 F300;

G1 Y-5.5 F150
G1 Y-7.5 F50;
G1 Y8 F300;

G1 Y-7 F150
G1 Y-9 F50;
G1 Y8 F300;

G1 Y-8.5 F150
G1 Y-10.5 F50;
G1 Y8 F300;

G1 Y-10 F150
G1 Y-12.0 F50;
G1 Y8 F300;

G1 Y-11.5 F150
G1 Y-13.5 F50;
G1 Y20 F300;