# usage: python tools/gcode_streamer.py gcode/01_line_x.gcode --port COM3
# add --dry-run to print the commands without sending
# add --list-ports to find the uno
import argparse
import re
import sys
import time


def clean(line):
    line = re.sub(r"\(.*?\)", "", line)   # (comments)
    line = line.split(";")[0]             # ; comments
    return line.strip()


def load(path):
    with open(path) as f:
        lines = [clean(l) for l in f]
    return [l for l in lines if l]


def list_ports():
    from serial.tools import list_ports as lp
    for p in lp.comports():
        print(p.device, p.description)


def wait_ok(ser, timeout):
    end = time.time() + timeout
    while time.time() < end:
        resp = ser.readline().decode(errors="replace").strip()
        if not resp:
            continue
        if resp.startswith(("ok", "error", "ALARM")):
            return resp
        print("   <", resp)
    return None   # timed out


def stream(path, port, baud, timeout, dry):
    lines = load(path)
    print(len(lines), "commands")

    if dry:
        for i, l in enumerate(lines, 1):
            print(i, l)
        return 0

    import serial
    with serial.Serial(port, baud, timeout=0.5) as ser:
        time.sleep(2)               # grbl resets when the port opens
        ser.reset_input_buffer()
        ser.write(b"\r\n\r\n")
        time.sleep(0.5)
        ser.reset_input_buffer()

        errors = 0
        for i, cmd in enumerate(lines, 1):
            ser.write((cmd + "\n").encode())
            print(f"[{i}/{len(lines)}] {cmd}")

            resp = wait_ok(ser, timeout)
            if resp is None:
                ser.write(b"!")     # feed hold
                print("timed out, feed hold sent")
                return 2
            if resp != "ok":
                errors += 1
                print("   <", resp)
                if resp.startswith("ALARM"):
                    print("alarm, send $X to unlock")
                    return 3

        # grbl returns ok before the move finishes, so wait for idle
        while True:
            ser.write(b"?")
            if ser.readline().decode(errors="replace").startswith("<Idle"):
                break
            time.sleep(0.2)

        print("done,", errors, "errors")
        return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--port")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--timeout", type=float, default=60)   # secs per ok
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list-ports", action="store_true")
    a = ap.parse_args()

    if a.list_ports:
        list_ports()
        return 0
    if not a.file:
        ap.error("need a gcode file")
    if not a.dry_run and not a.port:
        ap.error("need --port (or --dry-run)")
    return stream(a.file, a.port, a.baud, a.timeout, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
