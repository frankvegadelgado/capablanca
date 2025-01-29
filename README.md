# Capablanca: Minimum Vertex Cover Solver

![Honoring the Memory of Jose Raul Capablanca (Third World Chess Champion from 1921 to 1927)](docs/capablanca.jpg)

This work builds upon [The Minimum Vertex Cover Problem](https://www.researchgate.net/publication/388420196_The_Minimum_Vertex_Cover_Problem).

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

# Our Algorithm - Polynomial Runtime

## Algorithm Overview

1. **Input Validation:** Ensures the input is a valid sparse adjacency matrix.
2. **Graph Construction:** Converts the matrix into a graph using `networkx`.
3. **Component Decomposition:** Breaks the graph into connected components.
4. **Minimum Spanning Tree (MST):** Computes an MST for each component.
5. **Bipartition and Matching:** Treats the MST as a bipartite graph and finds a maximum matching.
6. **Vertex Cover Construction:** Combines vertex covers from all components.
7. **Redundancy Removal:** Eliminates unnecessary vertices while maintaining coverage.

## Correctness

- Ensures all edges are covered by leveraging bipartite graph properties and maximum matchings.
- The redundancy removal step guarantees minimality.

## Runtime Analysis

- **Graph Construction:** $O(|V| + |E|)$
- **MST Computation:** $O(|E| \log |V|)$
- **Maximum Matching:** $O(|V|^{2.5})$ (Hopcroft-Karp algorithm)
- **Redundancy Removal:** $O(|V||E|)$

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

   Supported file formats: `.txt`, `.xz`, `.lzma`, `.bz2`, `.bzip2`.

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
testMatrix2.txt: Vertex Cover Size 5
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

Estimating the Minimum Vertex Cover with an approximation factor smaller than √2 for an undirected graph encoded as a Boolean adjacency matrix stored in a file.

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
+ We present a polynomial-time algorithm achieving an approximation ratio below √2 for MVC, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.

+ This result contradicts the Unique Games Conjecture, suggesting that many optimization problems may admit better solutions, revolutionizing theoretical computer science.
```

---

# License

- MIT License.
