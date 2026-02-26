#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

/**
 * @brief Counts the number of valid arrays with minimum number of distinct values.
 */
class MinimumDistinctChainSolver {
public:
    static constexpr long long kMod = 1000000007LL;

    /**
     * @brief Computes base^exponent modulo kMod.
     *
     * @param base The base value.
     * @param exponent The exponent value (non-negative).
     * @return The value of base^exponent modulo kMod.
     */
    static long long modPow(long long base, long long exponent) {
        long long result = 1 % kMod;
        base %= kMod;
        while (exponent > 0) {
            if ((exponent & 1LL) != 0) {
                result = (result * base) % kMod;
            }
            base = (base * base) % kMod;
            exponent >>= 1LL;
        }
        return result;
    }

    /**
     * @brief Computes modular inverse of value modulo kMod (kMod is prime).
     *
     * @param value The value to invert (must be non-zero modulo kMod).
     * @return The modular inverse of value modulo kMod.
     */
    static long long modInverse(long long value) {
        return modPow(value, kMod - 2);
    }

    /**
     * @brief Builds factorial and inverse factorial arrays up to maxValue.
     *
     * @param maxValue The maximum factorial index to compute.
     * @param factorial Output vector where factorial[x] = x! modulo kMod.
     * @param inverseFactorial Output vector where inverseFactorial[x] = (x!)^{-1} modulo kMod.
     */
    static void buildFactorials(int maxValue, std::vector<long long>& factorial, std::vector<long long>& inverseFactorial) {
        factorial.assign(maxValue + 1, 1LL);
        inverseFactorial.assign(maxValue + 1, 1LL);

        for (int valueIndex = 1; valueIndex <= maxValue; ++valueIndex) {
            factorial[valueIndex] = (factorial[valueIndex - 1] * valueIndex) % kMod;
        }

        inverseFactorial[maxValue] = modInverse(factorial[maxValue]);
        for (int valueIndex = maxValue; valueIndex >= 1; --valueIndex) {
            inverseFactorial[valueIndex - 1] = (inverseFactorial[valueIndex] * valueIndex) % kMod;
        }
    }

    /**
     * @brief Computes the minimum number of distinct values required by the pattern.
     *
     * @param pattern The inequality pattern string of length n.
     * @return The value d = (maximum run length in pattern) + 1.
     */
    static int computeMinimumDistinctRequired(const std::string& pattern) {
        if (pattern.empty()) {
            return 1;
        }

        int bestRunLength = 1;
        int currentRunLength = 1;

        for (int positionIndex = 1; positionIndex < static_cast<int>(pattern.size()); ++positionIndex) {
            if (pattern[positionIndex] == pattern[positionIndex - 1]) {
                ++currentRunLength;
                bestRunLength = std::max(bestRunLength, currentRunLength);
            } else {
                currentRunLength = 1;
            }
        }

        return bestRunLength + 1;
    }

    /**
     * @brief Counts valid rank arrays over alphabet {1..alphabetSize}, allowing unused ranks.
     *
     * @param pattern The inequality pattern string.
     * @param alphabetSize The size M of the rank alphabet.
     * @return f(M) modulo kMod.
     */
    static long long countValidRankArraysAllowUnused(const std::string& pattern, int alphabetSize) {
        if (alphabetSize <= 0) {
            return 0;
        }

        std::vector<long long> waysEndingWithRank(alphabetSize + 1, 0LL);
        std::vector<long long> nextWaysEndingWithRank(alphabetSize + 1, 0LL);

        for (int rankValue = 1; rankValue <= alphabetSize; ++rankValue) {
            waysEndingWithRank[rankValue] = 1;
        }

        for (char inequalitySymbol : pattern) {
            if (inequalitySymbol == '<') {
                long long runningPrefixSum = 0;
                for (int rankValue = 1; rankValue <= alphabetSize; ++rankValue) {
                    nextWaysEndingWithRank[rankValue] = runningPrefixSum;
                    runningPrefixSum += waysEndingWithRank[rankValue];
                    if (runningPrefixSum >= kMod) {
                        runningPrefixSum -= kMod;
                    }
                }
            } else {
                long long runningSuffixSum = 0;
                for (int rankValue = alphabetSize; rankValue >= 1; --rankValue) {
                    nextWaysEndingWithRank[rankValue] = runningSuffixSum;
                    runningSuffixSum += waysEndingWithRank[rankValue];
                    if (runningSuffixSum >= kMod) {
                        runningSuffixSum -= kMod;
                    }
                }
            }
            waysEndingWithRank.swap(nextWaysEndingWithRank);
        }

        long long totalWays = 0;
        for (int rankValue = 1; rankValue <= alphabetSize; ++rankValue) {
            totalWays += waysEndingWithRank[rankValue];
            if (totalWays >= kMod) {
                totalWays -= kMod;
            }
        }
        return totalWays;
    }

    /**
     * @brief Computes C(largeNumber, smallK) modulo kMod for largeNumber < kMod and smallK small.
     *
     * @param largeNumber The n in C(n, k).
     * @param smallK The k in C(n, k).
     * @param inverseFactorial Precomputed inverse factorials up to smallK.
     * @return The value C(largeNumber, smallK) modulo kMod.
     */
    static long long computeBinomialLargeNSmallK(long long largeNumber, int smallK, const std::vector<long long>& inverseFactorial) {
        if (smallK < 0 || largeNumber < smallK) {
            return 0;
        }

        long long numeratorProduct = 1;
        for (int termIndex = 0; termIndex < smallK; ++termIndex) {
            numeratorProduct = (numeratorProduct * (largeNumber - termIndex)) % kMod;
        }
        return (numeratorProduct * inverseFactorial[smallK]) % kMod;
    }
};

/**
 * @brief Program entry point. Reads input, solves each test case, prints answers.
 *
 * @return Exit status code.
 */
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int testCaseCount = 0;
    std::cin >> testCaseCount;

    for (int testCaseIndex = 0; testCaseIndex < testCaseCount; ++testCaseIndex) {
        int patternLength = 0;
        long long maxBrightness = 0;
        std::cin >> patternLength >> maxBrightness;

        std::string pattern;
        std::cin >> pattern;

        if (static_cast<int>(pattern.size()) != patternLength) {
            patternLength = static_cast<int>(pattern.size());
        }

        const int minimumDistinctRequired = MinimumDistinctChainSolver::computeMinimumDistinctRequired(pattern);

        if (maxBrightness < minimumDistinctRequired) {
            std::cout << 0;
            if (testCaseIndex != testCaseCount - 1) std::cout << "\n";
            continue;
        }

        std::vector<long long> factorial;
        std::vector<long long> inverseFactorial;
        MinimumDistinctChainSolver::buildFactorials(minimumDistinctRequired, factorial, inverseFactorial);

        auto chooseFromDistinctCount = [&](int chooseCount) -> long long {
            return factorial[minimumDistinctRequired]
                * inverseFactorial[chooseCount] % MinimumDistinctChainSolver::kMod
                * inverseFactorial[minimumDistinctRequired - chooseCount] % MinimumDistinctChainSolver::kMod;
        };

        std::vector<long long> validCountAllowUnused(minimumDistinctRequired + 1, 0LL);
        for (int alphabetSize = 1; alphabetSize <= minimumDistinctRequired; ++alphabetSize) {
            validCountAllowUnused[alphabetSize] =
                MinimumDistinctChainSolver::countValidRankArraysAllowUnused(pattern, alphabetSize);
        }

        long long validCountUseAllSymbols = 0;
        for (int missingSymbolCount = 0; missingSymbolCount <= minimumDistinctRequired; ++missingSymbolCount) {
            const int remainingAlphabetSize = minimumDistinctRequired - missingSymbolCount;
            const long long inclusionExclusionTerm =
                chooseFromDistinctCount(missingSymbolCount)
                * validCountAllowUnused[remainingAlphabetSize] % MinimumDistinctChainSolver::kMod;

            if ((missingSymbolCount & 1) != 0) {
                validCountUseAllSymbols -= inclusionExclusionTerm;
                if (validCountUseAllSymbols < 0) {
                    validCountUseAllSymbols += MinimumDistinctChainSolver::kMod;
                }
            } else {
                validCountUseAllSymbols += inclusionExclusionTerm;
                if (validCountUseAllSymbols >= MinimumDistinctChainSolver::kMod) {
                    validCountUseAllSymbols -= MinimumDistinctChainSolver::kMod;
                }
            }
        }

        const long long chooseBrightnessLevels = MinimumDistinctChainSolver::computeBinomialLargeNSmallK(
            maxBrightness,
            minimumDistinctRequired,
            inverseFactorial
        );

        const long long answer =
            chooseBrightnessLevels * validCountUseAllSymbols % MinimumDistinctChainSolver::kMod;

            std::cout << answer;
            if (testCaseIndex != testCaseCount - 1) std::cout << "\n";    }

    return 0;
}