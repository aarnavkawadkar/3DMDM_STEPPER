; 01_line_x.gcode
; Single-axis line test. Motor is wired as the X axis.
; Expect: 20 mm forward, pause, 20 mm back to start.
G21          ; units = mm
G90          ; absolute positioning
G92 X0       ; set current position as zero
G1 X20 F300  ; 20 mm at 300 mm/min
G4 P1        ; dwell 1 second
G1 X0 F300   ; return to start
G4 P1
G1 X40 F600  ; faster 40 mm move
G1 X0 F600
M2           ; end program
