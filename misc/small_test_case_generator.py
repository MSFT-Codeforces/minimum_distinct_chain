
def main():
    inputs = []

    # 1) Minimum K=1 => always infeasible for n>=1
    inputs.append("1\n1 1\n<\n")

    # 2) Smallest n=1, feasible (single constraint, K=2)
    inputs.append("1\n1 2\n>\n")

    # 3) Monotone increasing, but K too small (cmin=n+1=3, K=2) => infeasible
    inputs.append("1\n2 2\n<<\n")

    # 4) Monotone decreasing, just feasible (cmin=3, K=3)
    inputs.append("1\n2 3\n>>\n")

    # 5) Perfect alternation, boundary K=2 (cmin=2)
    inputs.append("1\n3 2\n<><\n")

    # 6) Perfect alternation starting with '>', K=3
    inputs.append("1\n4 3\n><><\n")

    # 7) Long run at start, infeasible: max run=3 => cmin=4, K=3
    inputs.append("1\n5 3\n<<<>>\n")

    # 8) Same pattern as #7, just feasible with K=4 (K=cmin)
    inputs.append("1\n5 4\n<<<>>\n")

    # 9) Long run at end: max run=3 => cmin=4, K=4 (feasible)
    inputs.append("1\n5 4\n<<>>>\n")

    # 10) Mixed runs, internal long run (n=6), feasible with slack
    inputs.append("1\n6 5\n><<<><\n")

    # 11) Symmetry/reversal check (original)
    inputs.append("1\n6 4\n<><<<>\n")

    # 12) Symmetry/reversal check (reverse of #11 with signs flipped)
    inputs.append("1\n6 4\n<>>><>\n")

    # 13) All '>' with n=7, boundary K=cmin=8
    inputs.append("1\n7 8\n>>>>>>>\n")

    # 14) Random-ish mixed pattern, max run=2 => cmin=3, boundary K=3
    inputs.append("1\n8 3\n><>><<>>\n")

    # 15) Multi-testcase input to check reinitialization and mixed feasibility
    inputs.append(
        "4\n"
        "1 1\n>\n"        # infeasible (K=1)
        "3 4\n>>>\n"      # monotone decreasing, cmin=4, feasible (K=cmin)
        "4 2\n<><>\n"     # alternating, cmin=2, feasible (K=cmin)
        "6 3\n><<>>>\n"   # max run=3 => cmin=4, infeasible (K=3)
    )

    print("Test Cases:")
    for i, s in enumerate(inputs, 1):
        print(f"Input {i}:")
        print(s, end="" if s.endswith("\n") else "\n")
        if i != len(inputs):
            print()

if __name__ == "__main__":
    main()
