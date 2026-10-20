; 02_square.gcode
; 20 mm square. For a 2-axis setup (X and Y). With a single motor on X,
; Y moves are ignored by the hardware, so use 01_line_x.gcode instead,
; or run this once a second axis is wired.
G21
G90
G92 X0 Y0
G1 X20 Y0  F600
G1 X20 Y20 F600
G1 X0  Y20 F600
G1 X0  Y0  F600
; repeat the square twice more to check for lost steps
G1 X20 Y0  F600
G1 X20 Y20 F600
G1 X0  Y20 F600
G1 X0  Y0  F600
G1 X20 Y0  F600
G1 X20 Y20 F600
G1 X0  Y20 F600
G1 X0  Y0  F600
M2
