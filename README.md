# Capablanca: 2-Approximation Dominating Set Solver

![Honoring the Memory of Jose Raul Capablanca (Third World Chess Champion from 1921 to 1927)](docs/capablanca.jpg)

This work builds upon [A 2-Approximation Algorithm for Dominating Sets](https://dev.to/frank_vega_987689489099bf/a-2-approximation-algorithm-for-dominating-sets-1aga).

---

# Overview of the Minimum Dominating Set (MDS)

## Definition:

A **dominating set** in a graph $G = (V, E)$ is a subset $D \subseteq V$ such that every vertex not in $D$ is adjacent to at least one vertex in $D$. The **minimum dominating set (MDS)** is the smallest possible dominating set in terms of the number of vertices.

## Key Concepts:

1. **Graph Representation**:

   - $V$: Set of vertices.
   - $E$: Set of edges connecting the vertices.

2. **Dominating Set**:

   - A set $D$ where for every vertex $v \in V$, either $v \in D$ or $v$ is adjacent to some vertex in $D$.

3. **Minimum Dominating Set**:
   - The dominating set with the smallest cardinality (i.e., the fewest number of vertices).

## Applications:

- **Network Design**: Ensuring coverage in wireless sensor networks.
- **Social Networks**: Identifying influential nodes.
- **Game Theory**: Strategies in certain types of games.
- **Biology**: Modeling protein-protein interaction networks.

## Computational Complexity:

- **NP-Hard**: Finding the minimum dominating set is computationally intensive for large graphs.
- **Approximation Algorithms**: Used to find near-optimal solutions in polynomial time.

## Algorithms:

1. **Greedy Algorithm**:

   - Iteratively selects the vertex that covers the most uncovered vertices.
   - Provides a logarithmic approximation ratio.

2. **Integer Linear Programming (ILP)**:

   - Formulates the problem as an optimization problem.
   - Solvable using ILP solvers for exact solutions, though computationally expensive.

3. **Heuristics and Metaheuristics**:
   - Genetic algorithms, simulated annealing, etc., for large-scale problems.

## Challenges:

- **Scalability**: Exact algorithms are infeasible for very large graphs.
- **Dynamic Graphs**: Maintaining a minimum dominating set in graphs that change over time.

## Research Directions:

- **Parallel Algorithms**: Leveraging multi-core processors and distributed computing.
- **Machine Learning**: Using learning-based approaches to predict dominating sets.
- **Hybrid Methods**: Combining exact and heuristic methods for better performance.

## Conclusion:

The minimum dominating set problem is a fundamental issue in graph theory with wide-ranging applications. While it is computationally challenging, various algorithms and heuristics provide practical solutions for different scenarios. Ongoing research continues to improve the efficiency and applicability of these methods.

---

# Overview of the `find_dominating_set` Algorithm and Runtime Analysis

## Algorithm Purpose

The `find_dominating_set` algorithm computes a 2-approximation for the minimum dominating set in a general undirected graph. It transforms the input graph into a chordal structure and leverages the `approximate_dominating_set_chordal` algorithm, which is proven to provide a 2-approximation for chordal graphs. This approach ensures applicability to any graph while maintaining the approximation guarantee.

## Algorithm Structure

### `approximate_dominating_set_chordal` (Inner Algorithm)

- **Input**: A chordal graph $G$ with $n$ nodes and $m$ edges.
- **Process**:
  1. Verifies chordality $O(n + m)$.
  2. Computes a perfect elimination ordering (PEO) and reverses it $O(n)$.
  3. Iterates over nodes in reverse PEO:
     - For each undominated node $v$, selects a vertex from $N[v]$ (self and neighbors) that maximizes the number of undominated nodes covered.
     - Updates the dominating set and marks covered nodes as dominated.
- **Output**: A dominating set $D$ such that $|D| \leq 2 \cdot |OPT|$, where $OPT$ is the minimum dominating set.
- **Key Mechanism**: Greedy selection based on undominated coverage, leveraging chordal graph properties (PEO ensures structured neighborhoods).

### `find_dominating_set` (Outer Algorithm)

- **Input**: A general undirected graph $G$ with $n$ nodes and $m$ edges.
- **Process**:
  1. **Preprocessing**:
     - Handles trivial cases (empty graph or no edges): $O(1)$.
     - Identifies and removes isolated nodes, adding them to the dominating set: $O(n + m)$.
  2. **Component Processing**:
     - Identifies connected components: $O(n + m)$.
     - For each component with $n_i$ nodes and $m_i$ edges:
       - **Subgraph Extraction**: $O(n_i + m_i)$.
       - **Chordal Transformation**:
         - Creates a chordal graph with $2n_i$ nodes and $O(n_i^2)$ edges (includes a clique on $n_i$ nodes).
         - Construction time: $O(n_i^2)$.
       - **Inner Algorithm Call**: Applies `approximate_dominating_set_chordal` to the chordal graph.
       - **Mapping Back**: Extracts original node indices: $O(n_i)$.
  3. **Output**: Combines dominating sets from isolated nodes and components.
- **Output**: A dominating set for $G$ with size at most twice the minimum dominating set size.

## Runtime Analysis

### `approximate_dominating_set_chordal`

- **Preprocessing**:
  - Chordality check and PEO: $O(n + m)$.
  - Reverse PEO and initialization: $O(n)$.
- **Main Loop**:
  - Iterates $n$ times, but costly steps occur $|D| \leq n$ times.
  - For each selected $v$:
    - Computes $N[v]$: $O(d_v)$.
    - For each $w \in N[v]$ (size $d_v + 1$), counts undominated in $N[w]$: $O(d_w)$.
    - Total per $v$: $O(\sum\_{w \in N[v]} d_w) \leq O(m)$.
  - Overall: $O(n \cdot m)$ (e.g., in a clique, $m \approx n^2$).
- **Total**: $O(n + m) + O(nm) = O(nm)$.

### `find_dominating_set`

- **Preprocessing**:
  - Isolated nodes and removal: $O(n + m)$.
  - Connected components: $O(n + m)$.
- **Component Loop**:
  - $k$ components, $\sum n_i = n' \leq n$, $\sum m_i = m' \leq m$.
  - Per component:
    - Subgraph: $O(n_i + m_i)$.
    - Chordal graph: $n' = 2n_i$, $m' = n_i + m_i + {n_i \choose 2} = O(n_i^2)$, construction $O(n_i^2)$.
    - Inner call: $O(n'm') = O(2n_i \cdot n_i^2) = O(n_i^3)$.
    - Update: $O(n_i)$.
    - Total per component: $O(n_i^3)$.
  - Across all components: $\sum O(n_i^3) \leq O(n^3)$ (worst case: one component with $n$ nodes).
- **Total**: $O(n + m) + O(n^3) = O(n^3)$.

## Summary

- **Inner Algorithm**: $O(nm)$, efficient for chordal graphs with runtime dependent on edge density.
- **Outer Algorithm**: $O(n^3)$, dominated by the cubic cost per component due to the dense chordal graph, $O(n_i^2)$ edges, amplifying the inner $O(nm)$ runtime.
- **Correctness and Approximation**: Both algorithms produce dominating sets, with the outer algorithm preserving the 2-approximation by transforming general graphs into chordal ones, as verified through proofs and examples.

This $O(n^3)$ runtime reflects the current dense clique construction; optimizing the chordal transformation could potentially lower it to $O(n^2)$ or $O(nm)$.

---

## Problem Statement

Input: A Boolean Adjacency Matrix $M$.

Answer: Find a Minimum Dominating Set.

### Example Instance: 5 x 5 matrix

|        | c1  | c2  | c3  | c4  | c5  |
| ------ | --- | --- | --- | --- | --- |
| **r1** | 0   | 0   | 1   | 0   | 1   |
| **r2** | 0   | 0   | 0   | 1   | 0   |
| **r3** | 1   | 0   | 0   | 0   | 1   |
| **r4** | 0   | 1   | 0   | 0   | 0   |
| **r5** | 1   | 0   | 1   | 0   | 0   |

The input for undirected graph is typically provided in [DIMACS](http://dimacs.rutgers.edu/Challenges) format. In this way, the previous adjacency matrix is represented in a text file using the following string representation:

```
p edge 5 4
e 1 3
e 1 5
e 2 4
e 3 5
```

This represents a 5x5 matrix in DIMACS format such that each edge $(v,w)$ appears exactly once in the input file and is not repeated as $(w,v)$. In this format, every edge appears in the form of

```
e W V
```

where the fields W and V specify the endpoints of the edge while the lower-case character `e` signifies that this is an edge descriptor line.

_Example Solution:_

Dominating Set Found `1, 2`: Nodes `1` and `2` constitute an optimal solution.

---

# Compile and Environment

## Prerequisites

- Python ≥ 3.10

## Installation

```bash
pip install capablanca
```

## Execution

1. Clone the repository:

   ```bash
   git clone https://github.com/frankvegadelgado/capablanca.git
   cd capablanca
   ```

2. Run the script:

   ```bash
   approx -i ./benchmarks/testMatrix1
   ```

   utilizing the `approx` command provided by Capablanca's Library to execute the Boolean adjacency matrix `capablanca\benchmarks\testMatrix1`. The file `testMatrix1` represents the example described herein. We also support `.xz`, `.lzma`, `.bz2`, and `.bzip2` compressed text files.

   **Example Output:**

   ```
   testMatrix1: Dominating Set Found 1, 2
   ```

   This indicates nodes `1, 2` form a Dominating Set.

---

## Dominating Set Size

Use the `-c` flag to count the nodes in the Dominating Set:

```bash
approx -i ./benchmarks/testMatrix2 -c
```

**Output:**

```
testMatrix2: Dominating Set Size 2
```

---

# Command Options

Display help and options:

```bash
approx -h
```

**Output:**

```bash
usage: approx [-h] -i INPUTFILE [-a] [-b] [-c] [-v] [-l] [--version]

Find a 2-Approximate Dominating Set for undirected graph encoded in DIMACS format.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a logarithmic factor
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the Dominating Set
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Batch Execution

Batch execution allows you to solve multiple graphs within a directory consecutively.

To view available command-line options for the `batch_approx` command, use the following in your terminal or command prompt:

```bash
batch_approx -h
```

This will display the following help information:

```bash
usage: batch_approx [-h] -i INPUTDIRECTORY [-a] [-b] [-c] [-v] [-l] [--version]

Find a 2-Approximate Dominating Set for all undirected graphs encoded in DIMACS format and stored in a directory.

options:
  -h, --help            show this help message and exit
  -i INPUTDIRECTORY, --inputDirectory INPUTDIRECTORY
                        Input directory path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a logarithmic factor
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the Dominating Set
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Testing Application

A command-line utility named `test_approx` is provided for evaluating the Algorithm using randomly generated, large sparse matrices. It supports the following options:

```bash
usage: test_approx [-h] -d DIMENSION [-n NUM_TESTS] [-s SPARSITY] [-a] [-b] [-c] [-w] [-v] [-l] [--version]

The Capablanca Testing Application using randomly generated, large sparse matrices.

options:
  -h, --help            show this help message and exit
  -d DIMENSION, --dimension DIMENSION
                        an integer specifying the dimensions of the square matrices
  -n NUM_TESTS, --num_tests NUM_TESTS
                        an integer specifying the number of tests to run
  -s SPARSITY, --sparsity SPARSITY
                        sparsity of the matrices (0.0 for dense, close to 1.0 for very sparse)
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a logarithmic factor
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the Dominating Set
  -w, --write           write the generated random matrix to a file in the current directory
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Code

- Python implementation by **Frank Vega**.

---

# Complexity

```diff
+ We present a polynomial-time algorithm achieving a 2-approximation ratio for MDS, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.
```

---

# License

- MIT License.
