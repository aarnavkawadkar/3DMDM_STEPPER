; 04_accel_test.gcode
; Back-and-forth moves at increasing feed rates to find where the motor
; starts skipping steps. Mark the shaft or coupling with tape first and
; check it returns to the same angle. Lower $110 / $120 if it stalls.
G21
G90
G92 X0
G1 X30 F300
G1 X0  F300
G1 X30 F600
G1 X0  F600
G1 X30 F900
G1 X0  F900
G1 X30 F1200
G1 X0  F1200
G1 X30 F1500
G1 X0  F1500
G1 X30 F1800
G1 X0  F1800
M2
