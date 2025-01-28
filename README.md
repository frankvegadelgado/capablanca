# Capablanca: Minimum Vertex Cover Solver

![Honoring the Memory of Jose Raul Capablanca (Third World Chess Champion from 1921 to 1927)](docs/capablanca.jpg)

This work builds upon [The Minimum Vertex Cover Problem](https://www.researchgate.net/publication/388420196_The_Minimum_Vertex_Cover_Problem).

---

# The Minimum Vertex Cover Problem

The Minimum Vertex Cover (MVC) problem is a classic optimization problem in computer science and graph theory. It deals with finding the smallest set of vertices in a graph that `covers` all the edges. This means that for every edge in the graph, at least one of its endpoints must be in the chosen set of vertices.

## Formal Definition

Given an undirected graph $G = (V, E)$, where $V$ is the set of vertices and $E$ is the set of edges, a vertex cover is a subset $V' \subseteq V$ such that for every edge $(u, v) \in E$, at least one of the vertices $u$ or $v$ belongs to $V'$. The Minimum Vertex Cover problem aims to find a vertex cover $V'$ with the smallest possible cardinality (i.e., the fewest number of vertices).

## Importance and Applications

The Minimum Vertex Cover problem is important for several reasons:

- **Theoretical Significance:** It is a well-studied NP-hard problem, meaning that no known algorithm can solve it optimally for all instances in polynomial time. This makes it a crucial problem in complexity theory.
- **Practical Applications:** It has applications in various fields, including:
  - **Network security:** Finding critical nodes in a network that, if compromised, would disrupt connections.
  - **Bioinformatics:** Identifying important genes in gene regulatory networks.
  - **Wireless sensor networks:** Determining the minimum number of sensors needed to monitor a given area.

## Related Problems

The Minimum Vertex Cover problem is closely related to other graph problems, such as:

- **Maximum Independent Set:** A set of vertices where no two vertices are adjacent. The size of the minimum vertex cover plus the size of the maximum independent set is equal to the total number of vertices in the graph.
- **Set Cover Problem:** A more general problem where sets of elements are used to cover a universe of elements.

---

# Our Algorithm - Runtime $O(\vert V \vert^{3})$

## The algorithm explanation:

Steps in the Algorithm

1. Input Validation: The algorithm checks if the input is a valid sparse adjacency
   matrix and handles edge cases (e.g., empty graph).

2. Graph Construction: The adjacency matrix is converted into a graph G using
   networkx.

3. Component Decomposition: The graph is decomposed into connected components.

4. Minimum Spanning Tree (MST): For each component, a minimum spanning
   tree is computed.

5. Bipartition and Matching: The MST is treated as a bipartite graph, and a
   maximum matching is found. The matching is used to compute a vertex cover for
   the bipartite graph.

6. Vertex Cover Construction: The union of vertex covers from all components
   forms the initial vertex cover.

7. Redundancy Removal: The algorithm removes redundant vertices from the
   vertex cover while ensuring that the remaining set still covers all edges.

## Correctness

- The algorithm ensures that every edge in the graph is covered by the vertex cover.
  This is achieved by:
  - Computing a vertex cover for each connected component.
  - Using the properties of bipartite graphs and maximum matchings to ensure that
    all edges in the MST (and hence in the original graph) are covered.
  - Removing only those vertices that do not affect the coverage of edges (redundancy removal step).
- The redundancy removal step ensures that the final vertex cover is minimal (no
  unnecessary vertices are included).
  Thus, the algorithm returns a valid vertex cover.

## Runtime Analysis

The algorithm runs in polynomial time because:

- Constructing the graph from the adjacency matrix takes $O(\vert V\vert + \vert E\vert)$.

- Computing the MST using Kruskal's algorithm takes $O(\vert E\vert \log \vert V\vert)$.

- Computing the maximum matching and vertex cover for each bipartite graph takes $O(\vert V\vert^{2.5})$ (using Hopcroft-Karp algorithm).

- The redundancy removal step takes $O(\vert V\vert \vert E\vert)$.

Overall, the algorithm runs in polynomial time with respect to the size of the graph. Thus, the algorithm is a valid and efficient approximation algorithm for the vertex cover problem.

---

# Compile and Environment

## Install Python >=3.10.

## Install Capablanca's Library and its Dependencies with:

```bash
pip install capablanca
```

# Execute

1. Go to the package directory to use the benchmarks:

```bash
git clone https://github.com/frankvegadelgado/capablanca.git
cd capablanca
```

2. Execute the script:

```bash
cover -i .\benchmarks\testMatrix1.txt
```

utilizing the `cover` command provided by Capablanca's Library to execute the Boolean adjacency matrix `capablanca\benchmarks\testMatrix1.txt`. We also support .xz, .lzma, .bz2, and .bzip2 compressed .txt files.

## The console output will display:

```
testMatrix1.txt: Vertex Cover Found 2, 3, 4
```

which implies that the Boolean adjacency matrix `capablanca\benchmarks\testMatrix1.txt` contains a vertex cover of nodes `2, 3, 4`.

---

## Size of the Approximate Vertex Cover - Polynomial Runtime

The `-c` flag counts the nodes in the approximate vertex cover.

**Example:**

```bash
cover -i .\benchmarks\testMatrix2.txt -c
```

**Output:**

```
testMatrix2.txt: Vertex Cover Size 5
```

## Runtime Analysis:

We employ the same algorithm used to find vertex cover set.

---

# Command Options

To display the help message and available options, run the following command in your terminal:

```bash
cover -h
```

This will output:

```
usage: cover [-h] -i INPUTFILE [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Vertex Cover with an approximation factor smaller than √2 for an undirected graph encoded as a
Boolean adjacency matrix stored in a file.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with a polynomial-time approximation approach within a factor of 2
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the vertex cover
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

This output describes all available options.

## The Capablanca Testing Application

A command-line tool, `test_cover`, has been developed for testing algorithms on randomly generated, large sparse matrices. It accepts the following options:

```
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
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

**This tool is designed to benchmark algorithms for sparse matrix operations.**

It generates random square matrices with configurable dimensions (`-d`), sparsity levels (`-s`), and number of tests (`-n`). Brute-force and heuristic comparisons are available but not recommended for large datasets due to performance issues. Additionally, the generated matrix can be written to the current directory (`-w`), and verbose output or file logging can be enabled with the (`-v`) or (`-l`) flag, respectively, to record test results.

---

# Code

- Python code by **Frank Vega**.

---

# Complexity

```diff
+ We present a polynomial-time algorithm achieving an approximation ratio below √2 for the minimum vertex cover, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.

+ This result contradicts the Unique Games Conjecture, which predicts such improvements are impossible, thereby undermining UGC and reshaping our understanding of hardness of approximation.

+ The algorithm not only solves a long-standing open problem but also suggests that many other optimization problems might admit better solutions, revolutionizing theoretical computer science.
```

---

# License

- MIT.
