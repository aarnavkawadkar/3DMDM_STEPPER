# STEPPER GCODE TESTING

Test code for the 3DMDM stepper extruder: NEMA 17 + Arduino Uno + STEP/DIR driver, controlled with GRBL and G-code.

## STAGES

1. **Basic step/dir test** (`firmware/stepper_basic_test`): confirm the motor, driver, and power supply work using plain Arduino code.
2. **Flash GRBL** (`docs/GRBL_SETUP.md`): same wiring, now controlled by G-code.
3. **Calibrate** steps/mm and tune speed and acceleration.
4. **Validate motion** by streaming the test G-code files.
5. **Integrate** with the printer axis or feed mechanism.

## REPO LAYOUT

    firmware/stepper_basic_test/   Arduino sketch (serial-driven step/dir test)
    gcode/                         Test patterns: line, square, feed axis, accel sweep
    tools/gcode_streamer.py        Send G-code to GRBL over serial
    tools/steps_calculator.py      Compute and correct $100 (steps/mm)
    tools/gcode_generator.py       Generate custom line, square, and feed sweep files
    docs/GRBL_SETUP.md             Flashing, wiring, calibration, troubleshooting
    docs/grbl_settings_starter.txt Starting GRBL $ settings

## QUICK START

    pip install -r requirements.txt

    # 1. Basic test: upload the sketch, open serial monitor at 115200, send: t

    # 2. After flashing GRBL, find your port
    python tools/gcode_streamer.py --list-ports

    # 3. Preview without sending
    python tools/gcode_streamer.py gcode/01_line_x.gcode --dry-run

    # 4. Run it
    python tools/gcode_streamer.py gcode/01_line_x.gcode --port COM3

## WIRING (GRBL DEFAULT, X AXIS)

| Signal | Uno Pin |
|--------|---------|
| STEP   | D2      |
| DIR    | D5      |
| ENABLE | D8      |

Power the motor from the external supply only, share a common ground, and set the driver current limit before the first run.

## TEST CHECKLIST

- [ ] Basic sketch: forward, reverse, and `t` sequence return to start
- [ ] GRBL flashed, `$$` prints settings
- [ ] `$100` calibrated (error under 0.1 mm over 100 mm)
- [ ] `01_line_x.gcode` runs and returns to start
- [ ] `04_accel_test.gcode` completes with no skipped steps
- [ ] `$110` and `$120` tuned (20 percent margin below stall point)
- [ ] `02_square.gcode` verified on a 2-axis setup
- [ ] `03_feed_axis_extruder.gcode` verified with heater off
- [ ] Motor mounted to the target axis or feed mechanism

## NOTES

- Safety: keep the heater off and no material loaded during first motion tests.
- With a single motor on X, only the X component of any move executes.
- Team: 3DMDM, Virginia Tech.
