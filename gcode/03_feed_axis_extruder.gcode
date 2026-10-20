; 03_feed_axis_extruder.gcode
; For the extruder/feed mechanism. The motor is wired as the X axis in GRBL
; but represents filament/composite feed length (mm of travel).
; Slow, steady feed to check for stalls and consistent flow.
; START WITH THE HEATER OFF and no material loaded.
G21
G90
G92 X0
G1 X5   F60   ; 5 mm slow feed
G4 P2
G1 X15  F120  ; to 15 mm
G4 P2
G1 X30  F180  ; to 30 mm
G4 P2
G1 X0   F300  ; retract to start
M2
