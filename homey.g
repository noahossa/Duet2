M400        ; Wait for current move to finish
M913 Y60    ; Drop motor current to 30%
M400 
G91    ; relative positioning
G1 H1 Y-130 F8000 ;Move quickly to z axis endstop and stop there (first pass)
G1 H2 Y5 F10000 ; Go back a few mm
G1 H1 Y-130 F5000 ; move slowly to z axis endstop once more (second pass)
G90 ; absolute positioning
M400
M913 Y100 ; return motor current to 100%
M400