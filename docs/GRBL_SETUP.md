# GRBL SETUP (ARDUINO UNO + NEMA 17)

## 1. FLASH GRBL

1. Arduino IDE: Sketch > Include Library > Add .ZIP Library, then select the `grbl` folder from the GRBL 1.1 release (github.com/gnea/grbl).
2. File > Examples > grbl > grblUpload
3. Select board "Arduino Uno" and the correct port, then Upload.
4. Open a serial terminal at 115200 baud. You should see: `Grbl 1.1h ['$' for help]`

## 2. WIRING (GRBL DEFAULT UNO PINS, X AXIS)

| Signal | Uno Pin |
|--------|---------|
| STEP   | D2      |
| DIR    | D5      |
| ENABLE | D8      |

- Common ground between the Uno, the driver logic, and the motor supply.
- Motor power comes from the external supply only. Never power the motor from the Uno 5V.
- Set the driver current limit (Vref) BEFORE running the motor.
- Microstep jumpers must match the steps/mm calculation below.

## 3. CALIBRATE STEPS/MM

Formula:

    steps/mm = (motor steps/rev x microsteps) / mm per rev

Examples:

| Mechanism | mm per rev | Steps/mm at 16x microstepping |
|-----------|-----------|-------------------------------|
| GT2 belt, 20T pulley | 40 | 80 |
| T8 lead screw, 8 mm lead | 8 | 400 |
| Direct drive feed gear | pi x effective diameter | measure |

Or use the calculator:

    python tools/steps_calculator.py --microsteps 16 --mm-per-rev 8

Then set it in GRBL:

    $100=400

## 4. CALIBRATE BY MEASUREMENT

1. Send `G91` then `G1 X100 F300` (relative mode, move 100 mm commanded).
2. Measure how far the axis actually moved.
3. New steps/mm = old steps/mm x (commanded / measured).
4. Set `$100=<new value>` and repeat until the error is under 0.1 mm.

## 5. SPEED AND ACCELERATION SETTINGS

| Setting | Meaning | Start with |
|---------|---------|-----------|
| `$110` | X max rate (mm/min) | 600 |
| `$120` | X acceleration (mm/s^2) | 50 |
| `$0`   | Step pulse (microseconds) | 10 |
| `$1`   | Step idle delay (ms) | 255 (keeps motor energized) |
| `$3`   | Direction invert mask | 0 or 1 to flip direction |
| `$4`   | Step enable invert | 0 or 1 to match your driver |

Raise `$110` and `$120` in small steps using `gcode/04_accel_test.gcode`. Back off 20 percent from the point where the motor skips or stalls.

## 6. USEFUL REALTIME AND SYSTEM COMMANDS

| Command | Action |
|---------|--------|
| `$$` | View all settings |
| `$#` | View coordinate offsets |
| `?` | Status report (position, state) |
| `!` | Feed hold |
| `~` | Resume |
| Ctrl-X | Soft reset |
| `$X` | Clear alarm lock |
| `$H` | Homing (needs limit switches, `$22=1`) |

## 7. TROUBLESHOOTING

- Motor buzzes but does not turn: coil wires swapped or wrong pairing, or speed and acceleration too high.
- Moves the wrong distance: `$100` is wrong or microstep jumpers do not match.
- Moves the wrong direction: change `$3`.
- No motion at all: check `$4` (enable polarity), driver power, and common ground.
- Alarm on startup: send `$X`, and confirm `$21` (hard limits) is 0 when no switches are wired.
- Skipped steps at speed: lower `$110` and `$120`, or raise driver current.
