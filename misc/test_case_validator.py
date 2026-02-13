
import sys
import re

MOD = 10**9 + 7

def invalid():
    print("False")
    sys.exit(0)

def main():
    data = sys.stdin.read()
    # Disallow NUL characters
    if "\x00" in data:
        invalid()

    lines = data.splitlines()

    # No extra blank lines allowed anywhere (strict format)
    if any(line == "" for line in lines):
        invalid()

    if len(lines) < 1:
        invalid()

    # Line 1: t (exactly digits, no leading/trailing spaces)
    if not re.fullmatch(r"[0-9]+", lines[0]):
        invalid()
    t = int(lines[0])
    if not (1 <= t <= 40):
        invalid()

    # Expect exactly 2*t more lines
    if len(lines) != 1 + 2 * t:
        invalid()

    idx = 1
    for _ in range(t):
        # Line: "n K" (exactly two nonnegative integers separated by single space)
        if not re.fullmatch(r"[0-9]+ [0-9]+", lines[idx]):
            invalid()
        n_str, k_str = lines[idx].split(" ")
        n = int(n_str)
        K = int(k_str)
        if not (1 <= n <= 250):
            invalid()
        if not (1 <= K <= 10**9):
            invalid()
        if not (K < MOD):
            invalid()
        idx += 1

        # Line: s of length n, only '<' and '>', no spaces
        s = lines[idx]
        if not re.fullmatch(r"[<>]+", s):
            invalid()
        if len(s) != n:
            invalid()
        idx += 1

    print("True")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("False")
