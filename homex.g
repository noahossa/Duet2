M400        ; Wait for current move to finish
M913 X30    ; Drop motor curren to 30%
M400 
G91    ; relative positioning
G1 H1 X-360 F3000 ;Move quickly to z axis endstop and stop there (first pass)
G1 H2 X5 F4000 ; Go back a few mm
G1 H1 X-360 F3000 ; move slowly to z axis endstop once more (second pass)
G90 ; absolute positioning
M400
M913 X100 ; return motor current to 100%
M400