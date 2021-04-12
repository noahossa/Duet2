; Configuration file for Duet 3 (firmware version 3)
; executed by the firmware on start-up
; 
; Documentation 
; Last Updated: 3/29/2021 8:14PM
; Change Author: Michael Tang
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
; {}:Board Marking []:Polar drive mapping <--THIS IS WHAT ACTUALLY MATTERS
M569 P0 S0                          		; physical drive 0 {X Motor} [Z-DIR] goes forwards
M569 P1 S1                          		; physical drive 1 {Y Motor} [X-DIR] goes forwards
M569 P2 S0                          		; physical drive 2 {Z Motor} [Y-DIR] goes forwards SET TO S1 TO LOWER WHEN POSITIVE FOR TESTING
 
M92 X58.22 Y1600.00 Z80.00               		; set steps per mm for x, y, z [X is steps per degree for the V1 Chuck with 131 teeth]
M350 X128 Y128 Z128     	                    ; configure microstepping with interpolation
;M669 K7 R0:150 F30 A30 [Disabled due to interpolation which maybe unnecessary]                ; set Polar kinematics parameters

M906 X800 Y1000 Z800                            ; Set motor currents (mA)
M201 X800.00 Y400.00 Z800.00                    ; Accelerations (mm/s^2)
M203 X15000 Y150 Z15000                         ; Maximum speeds (mm/min)
M566 X600 Y600 Z600                             ; Maximum jerk speeds mm/minute

M84 S30                               		; Set idle timeout; length of inactivity time before the stepper motors idle

; Axis Limits
M208 X0 Y0 Z0 H0                        ; set axis minima
M208 X360 Y120 Z1748 H1                 ; set axis maxima
 
; Endstops
;M574 X0 Y0 Z0 S0                            ; !!NO endstops on this machine!!

 
; Tools
;M563 P0 S"Router"                           ; define tool 0
;G10 P0 X0 Y0 Z0                             ; set tool 0 axis offsets
;G10 P0 R0 S0                                ; set initial tool 0 active and standby temperatures to 0C
 
; CNC

;M564 S0 H0								    ; Allow movement without homing (without axis maxima)

; Custom settings are not defined
 
 
 