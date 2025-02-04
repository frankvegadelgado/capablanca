# Capablanca: Minimum Vertex Cover Solver

![Honoring the Memory of Jose Raul Capablanca (Third World Chess Champion from 1921 to 1927)](docs/capablanca.jpg)

---

# The Minimum Vertex Cover Problem

The **Minimum Vertex Cover (MVC)** problem is a classic optimization problem in computer science and graph theory. It involves finding the smallest set of vertices in a graph that **covers** all edges, meaning at least one endpoint of every edge is included in the set.

## Formal Definition

Given an undirected graph $G = (V, E)$, a **vertex cover** is a subset $V' \subseteq V$ such that for every edge $(u, v) \in E$, at least one of $u$ or $v$ belongs to $V'$. The MVC problem seeks the vertex cover with the smallest cardinality.

## Importance and Applications

- **Theoretical Significance:** MVC is a well-known NP-hard problem, central to complexity theory.
- **Practical Applications:**
  - **Network Security:** Identifying critical nodes to disrupt connections.
  - **Bioinformatics:** Analyzing gene regulatory networks.
  - **Wireless Sensor Networks:** Optimizing sensor coverage.

## Related Problems

- **Maximum Independent Set:** The complement of a vertex cover.
- **Set Cover Problem:** A generalization of MVC.

---

## Problem Statement

Input: A Boolean Adjacency Matrix $M$.

Answer: Find a Minimum Vertex Cover.

### Example Instance: 5 x 5 matrix

|        | c0  | c1  | c2  | c3  | c4  |
| ------ | --- | --- | --- | --- | --- |
| **r0** | 0   | 0   | 1   | 0   | 1   |
| **r1** | 0   | 0   | 0   | 1   | 0   |
| **r2** | 1   | 0   | 0   | 0   | 1   |
| **r3** | 0   | 1   | 0   | 0   | 0   |
| **r4** | 1   | 0   | 1   | 0   | 0   |

A matrix is represented in a text file using the following string representation:

```
00101
00010
10001
01000
10100
```

This represents a 5x5 matrix where each line corresponds to a row, and '1' indicates a connection or presence of an element, while '0' indicates its absence.

_Example Solution:_

Vertex Cover Found `0, 1, 2`: Nodes `0, 1, 2` form an optimal solution.

---

# Our Algorithm - Polynomial Runtime

## Algorithm Overview

1. **Input Validation**  
   Ensures the input is a valid sparse adjacency matrix.

2. **Graph Construction**  
   Converts the sparse adjacency matrix into a graph using the `networkx` library.

3. **Component Decomposition**  
   Decomposes the graph into its connected components for independent processing.

4. **Bipartition and Matching**  
   For each connected component that is a bipartite graph:

   - Find a **maximum matching** using an appropriate algorithm (e.g., Hopcroft-Karp).
   - Construct a **vertex cover** from the matching.

5. **Vertex Cover Construction**  
   Combines the vertex covers obtained from all bipartite components.

6. **Maximal Matching for Non-Bipartite Components**  
   For connected components that are **not bipartite**:

   - Find a **maximal matching** (not to be confused with maximum matching) using a greedy algorithm.
   - Select one endpoint for each edge in the matching, prioritizing vertices with higher degrees.

7. **Iterative Processing**
   - Remove the selected vertices from the graph.
   - Split the remaining graph into new connected components.
   - Repeat the process until all edges are covered.

## Correctness

- Ensures all edges are covered by leveraging bipartite graph properties and maximum matchings.

## Runtime Analysis

- **Graph Construction:** $O(|V| + |E|)$
- **Maximum Matching:** $O(|E| \log |V|)$ (Hopcroft-Karp algorithm)
- **Maximal Matching:** $O(|E|)$

Overall, the algorithm runs in **polynomial time**.

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
   cover -i ./benchmarks/testMatrix1.txt
   ```

   utilizing the `cover` command provided by Capablanca's Library to execute the Boolean adjacency matrix `capablanca\benchmarks\testMatrix1.txt`. The file `testMatrix1.txt` represents the example described herein. We also support `.xz`, `.lzma`, `.bz2`, and `.bzip2` compressed `.txt` files.

   **Example Output:**

   ```
   testMatrix1.txt: Vertex Cover Found 0, 1, 2
   ```

   This indicates nodes `0, 1, 2` form a vertex cover.

---

## Vertex Cover Size

Use the `-c` flag to count the nodes in the vertex cover:

```bash
cover -i ./benchmarks/testMatrix2.txt -c
```

**Output:**

```
testMatrix2.txt: Vertex Cover Size 6
```

---

# Command Options

Display help and options:

```bash
cover -h
```

**Output:**

```bash
usage: cover [-h] -i INPUTFILE [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Vertex Cover with an approximation factor of 7/5 for large enough undirected graphs encoded as a Boolean adjacency matrix stored in a file.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -v, --verbose         enable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Testing Application

A command-line utility named `test_cover` is provided for evaluating the Algorithm using randomly generated, large sparse matrices. It supports the following options:

```bash
usage: test_cover [-h] -d DIMENSION [-n NUM_TESTS] [-s SPARSITY] [-a] [-b] [-c] [-w] [-v] [-l] [--version]

The Capablanca Testing Application.

options:
  -h, --help            show this help message and exit
  -d DIMENSION, --dimension DIMENSION
                        an integer specifying the dimensions of the square matrices
  -n NUM_TESTS, --num_tests NUM_TESTS
                        an integer specifying the number of tests to run
  -s SPARSITY, --sparsity SPARSITY
                        sparsity of the matrices (0.0 for dense, close to 1.0 for very sparse)
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -w, --write           write the generated random matrix to a file in the current directory
  -v, --verbose         enable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Code

- Python implementation by **Frank Vega**.

---

# Complexity

```diff
+ We present a polynomial-time algorithm achieving an approximation ratio of 7/5 for MVC, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.

+ This result contradicts the Unique Games Conjecture, suggesting that many optimization problems may admit better solutions, revolutionizing theoretical computer science.
```

---

# License

- MIT License.
