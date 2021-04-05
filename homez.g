M400        ; Wait for current move to finish
M913 Z60    ; Drop motor curren to 30%
M400 
G91    ; relative positioning
G1 H1 Z-1750 F6000 ;Move quickly to z axis endstop and stop there (first pass)
G1 H2 Z5 F8000 ; Go back a few mm
G1 H1 Z-1750 F4000 ; move slowly to z axis endstop once more (second pass)
G90 ; absolute positioning
M400
M913 Z100 ; return motor current to 100%
M400