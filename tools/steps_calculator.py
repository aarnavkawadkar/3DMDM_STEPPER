# steps/mm for grbl $100
# python tools/steps_calculator.py --microsteps 16 --mm-per-rev 8
# python tools/steps_calculator.py --microsteps 16 --gear-diameter 11
# fix an old value after measuring: --current 400 --commanded 100 --measured 97.5
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("--motor-steps", type=int, default=200)   # 1.8 deg nema 17
ap.add_argument("--microsteps", type=int, default=16)
ap.add_argument("--mm-per-rev", type=float)
ap.add_argument("--gear-diameter", type=float)            # feed gear, mm
ap.add_argument("--current", type=float)
ap.add_argument("--commanded", type=float)
ap.add_argument("--measured", type=float)
a = ap.parse_args()

if a.current and a.commanded and a.measured:
    new = a.current * a.commanded / a.measured
    print(f"error: {(a.measured - a.commanded) / a.commanded * 100:+.2f}%")
    print(f"$100={new:.3f}")
else:
    mmPerRev = a.mm_per_rev
    if mmPerRev is None and a.gear_diameter:
        mmPerRev = math.pi * a.gear_diameter   # one rev of the gear
    if mmPerRev is None:
        ap.error("need --mm-per-rev or --gear-diameter")

    stepsPerMm = a.motor_steps * a.microsteps / mmPerRev
    print(f"mm/rev: {mmPerRev:.4f}")
    print(f"steps/rev: {a.motor_steps * a.microsteps}")
    print(f"$100={stepsPerMm:.3f}")
