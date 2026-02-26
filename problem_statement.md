Time Limit: **1 second**

Memory Limit: **32 MB**

You are given a row of $n+1$ lanterns, numbered from $1$ to $n+1$. Between lantern $i$ and $i+1$ there is a character $s_i$:

- if $s_i = \texttt{<}$ then the brightness must satisfy $a_i < a_{i+1}$,
- if $s_i = \texttt{>}$ then the brightness must satisfy $a_i > a_{i+1}$.

You must assign an integer brightness array $a_1,a_2,\dots,a_{n+1}$ such that:

- $1 \le a_i \le K$ for all $i$,
- all adjacent comparisons follow the string $s$.

Such an array is called **valid**.

Define the **cost** of an array as the number of **distinct** values among $a_1,\dots,a_{n+1}$. Let $c_{\min}$ be the minimum possible cost over all valid arrays. If no valid array exists, $c_{\min}$ is undefined.

For each test case, output the number of valid arrays whose cost equals $c_{\min}$, modulo $10^9+7$. If no valid array exists, output $0$.

**Input Format:-**

The first line contains an integer $t$ — the number of test cases.

Each test case consists of:
- one line containing two integers $n$ and $K$,
- one line containing a string $s$ of length $n$ consisting only of characters $\texttt{"<"}$ and $\texttt{">"}$.

**Output Format:-**

For each test case, print one integer — the number of valid arrays with minimum possible cost, modulo $10^9+7$.

**Constraints:-**

- $1 \le t \le 40$
- $1 \le n \le 250$
- $1 \le K \le 10^9$
- $K < 10^9+7$
- $|s| = n$, and $s_i \in \{\texttt{<},\texttt{>}\}$

**Examples:-**  
**Example 1**
 - **Input:**
```
1
8 3
><>><<>>
```

 - **Output:**
```
3
```

**Example 2**
 - **Input:**
```
4
1 1
>
3 4
>>>
4 2
<><>
6 3
><<>>>
```

 - **Output:**
```
0
1
1
0
```

**Note:-**  
In the first example, $s=\texttt{"><>><<>>"}$ has maximum consecutive run length $2$ (for example $\texttt{">>"}$ and $\texttt{"<<"}$), so $$c_{\min}=2+1=3.$$ Since $K=3$, we must use exactly the values $\{1,2,3\}$. The forced parts are:
- from $a_3>a_4>a_5$ we get $(a_3,a_4,a_5)=(3,2,1)$,
- since $a_5=1$, from $a_5<a_6<a_7$ we get $(a_6,a_7)=(2,3)$,
- since $a_7=3$, from $a_7>a_8>a_9$ we get $(a_8,a_9)=(2,1)$.
Now $a_1>a_2<a_3$ with $a_3=3$ allows $(a_1,a_2)$ to be $(3,2)$, $(2,1)$, or $(3,1)$, giving exactly $3$ minimum-cost valid arrays.

In the second example, for the test case $n=1$, $K=1$, $s=\texttt{">"}$, we need $a_1>a_2$ but the only allowed value is $1$, so no valid array exists and the answer is $0$.

In the second example, for the test case $n=3$, $K=4$, $s=\texttt{">>>"}$, the maximum run length is $3$, so $c_{\min}=4$. With $K=4$ the only choice of $4$ distinct values is $\{1,2,3,4\}$, and the inequalities force the unique array $(4,3,2,1)$, so the answer is $1$.

In the second example, for the test case $n=4$, $K=2$, $s=\texttt{"<><>"}$, the maximum run length is $1$, so $c_{\min}=2$. With values $\{1,2\}$ the inequalities force the unique alternating array $(1,2,1,2,1)$, so the answer is $1$.

In the second example, for the test case $n=6$, $K=3$, $s=\texttt{"><<>>>"}$, the maximum run length is $3$ (the suffix $\texttt{">>>"}$), so $$c_{\min}=3+1=4.$$ Since $K=3<4$, no valid array can satisfy all strict inequalities within $[1,K]$, so the answer is $0$.