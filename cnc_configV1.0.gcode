; Configuration file for Duet 3 (firmware version 3)
; executed by the firmware on start-up
;
M111 S0                                  ; Debug off
M550 PNUAVTubeDriller                    ; Machine name and Netbios name (can be anything you like)
M551 PNUAV                               ; Machine password (used for FTP)

;Ethernet Netowrking settings
M552 P0.0.0.0                      ; IP address
M554 P192.168.0.255                ; Gateway
M553 P255.255.255.0                ; Netmask
M552 S1                    ; Turn network on
M555 P2                    ; Set output to look like Marlin

; General preferences
M555 P2                    ; Set output to look like Marlin
G21                        ; Work in millimetres
G90                        ; Send absolute coordinates...
M83                        ; ...but relative extruder moves


; Set motor drive mapping to polar:
; X direction: axial spin of the tube
; Y direction: retraction and plunge of tool head on the carriage
; Z direction: carriage motion along the rails
M584 X1 Y2 Z0 
 
; Add Drives and direction
M569 P0 S1                          		; physical drive 0 goes forwards
M569 P1 S1                          		; physical drive 1 goes forwards
M569 P2 S1                          		; physical drive 2 goes forwards
 
M350 M350 X128 Y128 Z128               		; configure microstepping with interpolation
M92 X10 Y10 Z10      	                    ; (SLOW AF FOR SAFETY) set steps per mm for x, y, z
M669 K7 R0:150 H0.3 F30 A30                 ; set Polar kinematics parameters

M906 X800 Y1000 Z800 E800                   ; Set motor currents (mA)
M201 X800 Y800 Z15 E1000                    ; Accelerations (mm/s^2)
M203 X15000 Y15000 Z100 E3600               ; Maximum speeds (mm/min)
M566 X600 Y600 Z30 E20                      ; Maximum jerk speeds mm/minute

M84 S30                               		; Set idle timeout; length of inactivity time before the stepper motors idle
 
; Axis Limits
M208 X-0:1100 Y0:120 Z0:1748                ; set axis minima and maxima
 
; Endstops
M574 X0 Y0 Z0 S0                            ; !!NO endstops on this machine!!

 
; Tools
M563 P0 S"Router"                           ; define tool 0
G10 P0 X0 Y0 Z0                             ; set tool 0 axis offsets
G10 P0 R0 S0                                ; set initial tool 0 active and standby temperatures to 0C
 
; CNC

M564 S0 H0								    ; Allow movement without homing (without axis maxima)

; Custom settings are not defined
 
 
 