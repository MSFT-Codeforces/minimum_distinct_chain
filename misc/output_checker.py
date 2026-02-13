
import os
import re
from typing import Tuple, List

MOD = 10**9 + 7

# Output must be a non-negative integer token (modulo MOD).
_UINT_RE = re.compile(r"^\d+$")


def _normalize_newlines(text: str) -> str:
    # Normalize CRLF/CR to LF for consistent parsing.
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _tokenize_input(text: str) -> List[str]:
    # Judge input is assumed valid; tokenize by any whitespace for robustness.
    return text.split()


def _compute_cmin(s: str) -> int:
    """
    For a chain of strict inequalities, the minimum number of distinct values needed
    equals (maximum length of a consecutive run of identical signs) + 1.
    Assumes s is non-empty (n >= 1 in constraints).
    """
    max_run = 1
    cur = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cur += 1
        else:
            if cur > max_run:
                max_run = cur
            cur = 1
    if cur > max_run:
        max_run = cur
    return max_run + 1


def check(input_text: str, output_text: str) -> Tuple[bool, str]:
    input_text = _normalize_newlines(input_text)
    output_text = _normalize_newlines(output_text)

    # ---- Parse input (only what we need) ----
    toks = _tokenize_input(input_text)
    if not toks:
        return (False, "Input parsing failed: empty input")

    it = iter(toks)
    try:
        t = int(next(it))
    except StopIteration:
        return (False, "Input parsing failed: missing t")
    except ValueError:
        return (False, "Input parsing failed: t is not an integer")

    if not (1 <= t <= 40):
        # Not strictly required for checking output, but helps catch malformed input_text.
        return (False, f"Input parsing failed: t={t} is outside constraints [1..40]")

    cases = []
    for case_idx in range(1, t + 1):
        try:
            n = int(next(it))
            K = int(next(it))
            s = next(it)
        except StopIteration:
            return (False, f"Input parsing failed: incomplete test case {case_idx}")
        except ValueError:
            return (False, f"Input parsing failed: n/K not integers in case {case_idx}")

        if not (1 <= n <= 250):
            return (False, f"Input parsing failed: case {case_idx} has n={n} outside [1..250]")
        if not (1 <= K <= 10**9):
            return (False, f"Input parsing failed: case {case_idx} has K={K} outside [1..1e9]")
        if K >= MOD:
            return (False, f"Input parsing failed: case {case_idx} has K={K} but must satisfy K < {MOD}")

        if len(s) != n:
            return (False, f"Input parsing failed: case {case_idx} has |s|={len(s)} but n={n}")
        bad_pos = next((i for i, ch in enumerate(s, start=1) if ch not in "<>"), None)
        if bad_pos is not None:
            return (False, f"Input parsing failed: case {case_idx} has invalid s[{bad_pos}]={s[bad_pos-1]!r}")
        cases.append((n, K, s))

    # ---- Strict output format ----
    # Allow at most one trailing newline at EOF; otherwise no extra whitespace/lines.
    if output_text.endswith("\n\n"):
        return (False, "Output format error: more than one trailing newline at EOF")

    lines = output_text.split("\n")
    if lines and lines[-1] == "":
        # Allow exactly one trailing newline.
        lines.pop()

    if len(lines) != t:
        return (False, f"Output format error: expected {t} line(s), got {len(lines)}")

    # ---- Per-case output validation ----
    for case_idx, line in enumerate(lines, start=1):
        if line == "":
            return (False, f"Case {case_idx}: empty line (expected an integer in [0..{MOD-1}])")
        if line.strip() != line:
            return (False, f"Case {case_idx}: leading/trailing whitespace is not allowed: {line!r}")
        if not _UINT_RE.match(line):
            return (False, f"Case {case_idx}: not a valid non-negative integer token: {line!r}")

        # Parse integer
        try:
            ans = int(line)
        except ValueError:
            return (False, f"Case {case_idx}: cannot parse integer from {line!r}")

        if not (0 <= ans < MOD):
            return (False, f"Case {case_idx}: value {ans} out of range [0..{MOD-1}]")

        # Trivially checkable correctness: infeasibility when K < c_min.
        n, K, s = cases[case_idx - 1]
        cmin = _compute_cmin(s)
        if K < cmin and ans != 0:
            return (
                False,
                f"Case {case_idx}: K={K} < c_min={cmin} implies no valid array exists; expected 0, got {ans}",
            )

    return (True, "OK")


if __name__ == "__main__":
    in_path = os.environ.get("INPUT_PATH")
    out_path = os.environ.get("OUTPUT_PATH")
    if not in_path or not out_path:
        print("False")
    else:
        with open(in_path, "r", encoding="utf-8") as f:
            inp = f.read()
        with open(out_path, "r", encoding="utf-8") as f:
            out = f.read()
        ok, _ = check(inp, out)
        print("True" if ok else "False")
