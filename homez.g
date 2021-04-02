M400        ; Wait for current move to finish
M913 Z30    ; Drop motor curren to 30%
M400 G91    ; relative positioning
G1 H1 Z-320.5 F10000 ;Move quickly to z axis endstop and stop there (first pass)
G1 H2 Z5 F12000 ; Go back a few mm
G1 H1 Z-320.5 F7000 ; move slowly to z axis endstop once more (second pass)
G90 ; absolute positioning
M400
M913 Z100 ; return motor current to 100%
M400