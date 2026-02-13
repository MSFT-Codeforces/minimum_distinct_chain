
def alt_string(n, start="<"):
    # Perfect alternation with run length 1
    other = ">" if start == "<" else "<"
    return "".join(start if i % 2 == 0 else other for i in range(n))

def flip_rev(s):
    # Reverse and swap <->>
    mp = {"<": ">", ">": "<"}
    return "".join(mp[ch] for ch in reversed(s))

inputs = []

# Input 1: n=1, K=1 (always infeasible)
inputs.append("\n".join([
    "1",
    "1 1",
    "<"
]))

# Input 2: n=1, K=2, '<' (feasible, boundary K=cmin=2)
inputs.append("\n".join([
    "1",
    "1 2",
    "<"
]))

# Input 3: n=1, K=2, '>' (feasible, boundary K=cmin=2)
inputs.append("\n".join([
    "1",
    "1 2",
    ">"
]))

# Input 4: n=2, alternating "<>" (cmin=2), K=2 exact boundary
inputs.append("\n".join([
    "1",
    "2 2",
    "<>"
]))

# Input 5: n=2, alternating "<>", K=1 (infeasible)
inputs.append("\n".join([
    "1",
    "2 1",
    "<>"
]))

# Input 6: monotone increasing, n=5, K=6 (cmin=6), feasible boundary
inputs.append("\n".join([
    "1",
    "5 6",
    "<" * 5
]))

# Input 7: monotone increasing, n=5, K=5 (cmin=6), infeasible just below
inputs.append("\n".join([
    "1",
    "5 5",
    "<" * 5
]))

# Input 8: maximum n=250, monotone decreasing, K=251 (cmin=251), feasible boundary
inputs.append("\n".join([
    "1",
    "250 251",
    ">" * 250
]))

# Input 9: large n=249 alternating, huge K=1e9 (tests large-K combinatorics)
inputs.append("\n".join([
    "1",
    "249 1000000000",
    alt_string(249, start="<")
]))

# Input 10: max run in the middle (max run 3), K=cmin-1 => infeasible
# s = "<>><<<>><<" has max run 3 ('<<<'), so cmin=4, K=3 infeasible
inputs.append("\n".join([
    "1",
    "10 3",
    "<>><<<>><<"
]))

# Input 11: max run at the end (run 4), K=cmin (feasible boundary)
# s = "><><>>" + "<<<<" => end run '<<<<' length 4 => cmin=5, K=5
inputs.append("\n".join([
    "1",
    "10 5",
    "><><>><<<<"
]))

# Input 12: max run at the start (run 5), K=cmin (feasible boundary)
# s = ">>>>>" + "<><><" => start run length 5 => cmin=6, K=6
inputs.append("\n".join([
    "1",
    "10 6",
    ">>>>><><><"
]))

# Input 13: symmetry/reversal pair in same input (t=2)
s1 = "<<>><<>"
s2 = flip_rev(s1)
inputs.append("\n".join([
    "2",
    f"{len(s1)} 10",
    s1,
    f"{len(s2)} 10",
    s2
]))

# Input 14: multiple varied small tests in one input (tests reinitialization, feasibility boundaries)
inputs.append("\n".join([
    "5",
    "1 1",
    ">",          # infeasible
    "3 2",
    "<<<",        # cmin=4, infeasible
    "3 4",
    "<<<",        # cmin=4, feasible boundary
    "4 2",
    "<>><",       # runs: '>>' => cmin=3, infeasible
    "4 3",
    "<>><",       # feasible boundary
]))

# Input 15: stress input, t=40, n=250 each, mixed patterns + mixed feasibility
stress_cases = []
for i in range(40):
    n = 250
    if i % 4 == 0:
        s = "<" * n               # cmin=251
        K = 251                   # feasible boundary
    elif i % 4 == 1:
        s = ">" * n               # cmin=251
        K = 250                   # infeasible just below
    elif i % 4 == 2:
        s = alt_string(n, "<")    # cmin=2
        K = 1_000_000_000         # huge K
    else:
        s = "<" * 60 + ">" * 60 + "<" * 60 + ">" * 70  # max run 70 => cmin=71
        K = 71                    # feasible boundary
    stress_cases.append(f"{n} {K}\n{s}")

inputs.append("40\n" + "\n".join(stress_cases))

print("Test Cases: ")
for i, inp in enumerate(inputs, 1):
    print(f"Input {i}:")
    print(inp)
    if i != len(inputs):
        print()
