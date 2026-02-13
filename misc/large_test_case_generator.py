
import random

def alternating(n, start="<"):
    other = ">" if start == "<" else "<"
    return "".join(start if i % 2 == 0 else other for i in range(n))

def random_block_string(n, max_block_len=50):
    s = []
    cur = random.choice(["<", ">"])
    left = n
    while left > 0:
        bl = random.randint(1, min(max_block_len, left))
        s.append(cur * bl)
        left -= bl
        cur = ">" if cur == "<" else "<"
    return "".join(s)

def flip_reverse(s: str) -> str:
    # reverse and swap <->>
    trans = str.maketrans("<>", "><")
    return s[::-1].translate(trans)

def cmin_from_s(s: str) -> int:
    best = 1
    cur = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cur += 1
        else:
            best = max(best, cur)
            cur = 1
    best = max(best, cur)
    return best + 1  # max run length + 1

def make_input(cases):
    out = [str(len(cases))]
    for n, K, s in cases:
        assert len(s) == n
        assert 1 <= n <= 250
        assert 1 <= K <= 10**9
        out.append(f"{n} {K}")
        out.append(s)
    return "\n".join(out)

random.seed(12345)

inputs = []

N = 250
T = 40

# Helper blocky strings with known max runs at different positions (all length 250)
sA = "<" * 80 + ">" * 70 + "<" * 100          # max run 100 => cmin 101
sB = ">" * 60 + "<" * 90 + ">" * 100          # max run 100 => cmin 101
sC = "<" * 120 + ">" * 80 + "<" * 50          # max run 120 => cmin 121
sD = ">" * 50 + "<" * 150 + ">" * 50          # max run 150 => cmin 151
sE = "<" + ">" * 249                          # max run 249 => cmin 250
sF = ">" + "<" * 249                          # max run 249 => cmin 250
base_patterns = [sA, sB, sC, sD, sE, sF]

# Input 1: heavy stress, max t and n, huge K, random blocky patterns
cases1 = []
for i in range(T):
    max_block = 5 + (i % 46)  # 5..50
    s = random_block_string(N, max_block_len=max_block)
    cases1.append((N, 10**9, s))
inputs.append(make_input(cases1))

# Input 2: monotone all '<', max n, huge K (forces cmin = 251)
cases2 = [(N, 10**9, "<" * N) for _ in range(T)]
inputs.append(make_input(cases2))

# Input 3: monotone all '>', max n, huge K (forces cmin = 251)
cases3 = [(N, 10**9, ">" * N) for _ in range(T)]
inputs.append(make_input(cases3))

# Input 4: perfectly alternating (both starts), max n, huge K (cmin = 2)
cases4 = []
for i in range(T):
    s = alternating(N, start="<" if i % 2 == 0 else ">")
    cases4.append((N, 10**9, s))
inputs.append(make_input(cases4))

# Input 5: infeasible due to K=1 with large n, various strings (should all output 0)
cases5 = []
for i in range(T):
    if i % 4 == 0:
        s = alternating(N, start=">")
    elif i % 4 == 1:
        s = random_block_string(N, max_block_len=30)
    elif i % 4 == 2:
        s = "<" * 125 + ">" * 125
    else:
        s = ">" * 200 + "<" * 50
    cases5.append((N, 1, s))
inputs.append(make_input(cases5))

# Input 6: boundary K = cmin exactly (tight feasible), mix of designed + random
cases6 = []
for i in range(T):
    if i < len(base_patterns):
        s = base_patterns[i]
    else:
        s = random_block_string(N, max_block_len=random.randint(2, 120))
    K = cmin_from_s(s)
    cases6.append((N, K, s))
inputs.append(make_input(cases6))

# Input 7: boundary K = cmin - 1 (tight infeasible), mix of designed + random
cases7 = []
forced = [
    "<" * N,
    ">" * N,
    alternating(N, "<"),
    alternating(N, ">"),
    ">" * 200 + "<" * 50,
    "<" * 125 + ">" * 125,
    "<" + ">" * 249,
    ">" + "<" * 249,
    "<" * 40 + ">" * 210,
    ">" * 111 + "<" * 139,
]
for i in range(T):
    if i < len(forced):
        s = forced[i]
    else:
        s = random_block_string(N, max_block_len=random.randint(2, 120))
    K = cmin_from_s(s) - 1  # since cmin>=2, K>=1
    cases7.append((N, K, s))
inputs.append(make_input(cases7))

# Input 8: boundary K = cmin + 1 (just above tight feasible), various shapes
cases8 = []
seed_patterns8 = [
    "<" * N,
    ">" * N,
    sD, sC, sA,
    alternating(N, "<"),
    alternating(N, ">"),
]
for i in range(T):
    if i < len(seed_patterns8):
        s = seed_patterns8[i]
    else:
        s = random_block_string(N, max_block_len=random.randint(10, 120))
    K = cmin_from_s(s) + 1
    cases8.append((N, K, s))
inputs.append(make_input(cases8))

# Input 9: symmetry/reversal pairs with huge K (40 cases = 20 pairs)
cases9 = []
for _ in range(T // 2):
    base = random_block_string(N, max_block_len=random.randint(5, 80))
    mirror = flip_reverse(base)
    cases9.append((N, 10**9, base))
    cases9.append((N, 10**9, mirror))
inputs.append(make_input(cases9))

# Input 10: mixed stress suite, max t and n, varied K (including huge), varied patterns
cases10 = []
Ks = [1, 2, 3, 5, 10, 50, 100, 150, 200, 249, 250, 251, 252, 10**9]
pattern_pool = [
    "<" * N,
    ">" * N,
    alternating(N, "<"),
    alternating(N, ">"),
    sA, sB, sC, sD, sE, sF,
]
for i in range(T):
    if i % 5 == 0:
        s = random_block_string(N, max_block_len=random.randint(5, 100))
    else:
        s = pattern_pool[i % len(pattern_pool)]

    if i % 7 == 0:
        K = cmin_from_s(s) - 1  # possibly infeasible
    elif i % 7 == 1:
        K = cmin_from_s(s)      # tight feasible
    elif i % 7 == 2:
        K = cmin_from_s(s) + 1
    else:
        K = Ks[(i * 3) % len(Ks)]

    # enforce constraints range
    K = max(1, min(10**9, K))
    cases10.append((N, K, s))
inputs.append(make_input(cases10))

print("Test Cases:")
for idx, content in enumerate(inputs, 1):
    print(f"Input {idx}:")
    print(content)
    if idx != len(inputs):
        print()
