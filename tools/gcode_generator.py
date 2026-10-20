# python tools/gcode_generator.py line --length 25 --feed 400 > gcode/my_line.gcode
# python tools/gcode_generator.py square --size 15 --repeats 3 > gcode/my_square.gcode
# python tools/gcode_generator.py sweep --length 30 --feeds 300 600 900 > gcode/my_sweep.gcode
import argparse

HEADER = ["G21", "G90", "G92 X0 Y0"]   # mm, absolute, zero here


def line(length, feed):
    return HEADER + [f"G1 X{length:g} F{feed:g}", "G4 P1", f"G1 X0 F{feed:g}", "M2"]


def square(size, feed, repeats):
    out = list(HEADER)
    for _ in range(repeats):
        out += [
            f"G1 X{size:g} Y0 F{feed:g}",
            f"G1 X{size:g} Y{size:g} F{feed:g}",
            f"G1 X0 Y{size:g} F{feed:g}",
            f"G1 X0 Y0 F{feed:g}",
        ]
    return out + ["M2"]


def sweep(length, feeds):
    out = list(HEADER)
    for f in feeds:   # out and back at each feed
        out += [f"G1 X{length:g} F{f:g}", f"G1 X0 F{f:g}"]
    return out + ["M2"]


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="kind", required=True)

p = sub.add_parser("line")
p.add_argument("--length", type=float, default=20)
p.add_argument("--feed", type=float, default=300)

p = sub.add_parser("square")
p.add_argument("--size", type=float, default=20)
p.add_argument("--feed", type=float, default=600)
p.add_argument("--repeats", type=int, default=1)

p = sub.add_parser("sweep")
p.add_argument("--length", type=float, default=30)
p.add_argument("--feeds", type=float, nargs="+", default=[300, 600, 900, 1200])

a = ap.parse_args()
if a.kind == "line":
    print("\n".join(line(a.length, a.feed)))
elif a.kind == "square":
    print("\n".join(square(a.size, a.feed, a.repeats)))
else:
    print("\n".join(sweep(a.length, a.feeds)))
