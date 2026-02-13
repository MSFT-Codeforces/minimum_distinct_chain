#include <algorithm>
#include <climits>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static const long long MOD = 1000000007LL;

/*
  Brute-force baseline:
  Enumerate all arrays a[0..n] with values in [1..K], enforcing inequalities on the fly.
  For each valid full array, compute the number of distinct values and track:
    - the minimum distinct count found
    - how many arrays achieve that minimum (mod MOD)

  This is intentionally non-optimized and is only suitable for very small (n, K).
*/
struct BruteSolver {
    int n;
    long long k;
    string s;

    vector<long long> a;
    int minDistinct;
    long long ways;

    int countDistinctInCurrentArray() {
        vector<long long> b = a;
        sort(b.begin(), b.end());
        int distinct = 0;
        for (int i = 0; i < (int)b.size(); i++) {
            if (i == 0 || b[i] != b[i - 1]) {
                distinct++;
            }
        }
        return distinct;
    }

    void dfs(int idx) {
        if (idx == n + 1) {
            int distinct = countDistinctInCurrentArray();
            if (distinct < minDistinct) {
                minDistinct = distinct;
                ways = 1;
            } else if (distinct == minDistinct) {
                ways++;
                if (ways >= MOD) {
                    ways -= MOD;
                }
            }
            return;
        }

        for (long long v = 1; v <= k; v++) {
            if (idx > 0) {
                char c = s[idx - 1];
                if (c == '<') {
                    if (!(a[idx - 1] < v)) {
                        continue;
                    }
                } else { // c == '>'
                    if (!(a[idx - 1] > v)) {
                        continue;
                    }
                }
            }
            a[idx] = v;
            dfs(idx + 1);
        }
    }

    long long solveOne(int nInput, long long kInput, const string &sInput) {
        n = nInput;
        k = kInput;
        s = sInput;

        a.assign(n + 1, 1);
        minDistinct = INT_MAX;
        ways = 0;

        dfs(0);

        if (minDistinct == INT_MAX) {
            return 0;
        }
        return ways % MOD;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    BruteSolver solver;
    while (t--) {
        int n;
        long long k;
        string s;
        cin >> n >> k;
        cin >> s;

        cout << solver.solveOne(n, k, s) << "\n";
    }

    return 0;
}