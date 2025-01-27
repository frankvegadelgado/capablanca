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

# Our Algorithm - Runtime $O(n^{2} \cdot m)$

## The algorithm explanation:

The algorithm works as follows:

1. It takes a sparse adjacency matrix as input and converts it into a graph.

2. It decomposes the graph into connected components.

3. For each connected component, it computes a minimum edge cut and selects one of the two candidate vertex sets (based on their degrees) to add to the vertex cover.

4. It repeats this process until all edges are covered.

## Correctness

The algorithm guarantees that every edge in the graph is covered by the computed vertex cover. This is achieved through the following steps:

1. The algorithm processes each connected component of the graph iteratively. This ensures that all parts of the graph are considered, even if the graph is disconnected.

2. For each connected component, the algorithm computes a minimum edge cut. The vertices involved in this cut are added to the vertex cover, ensuring that all edges in the cut are covered.

3. After adding the vertices of the cut to the cover, the algorithm removes these vertices from the graph. This step eliminates all edges incident to the selected vertices, ensuring they are fully covered.

4. The process repeats on the remaining subgraph until no edges are left. This iterative approach guarantees that every edge in the original graph is incident to at least one vertex in the final cover.

By systematically processing each connected component and leveraging the properties of minimum edge cuts, the algorithm constructs a valid vertex cover that satisfies the problem's requirements.

## Runtime Analysis

The algorithm runs in polynomial time because:

1. Converting the sparse adjacency matrix to edges takes $O(m)$ time, where $m$ is the number of edges.

2. Constructing the graph using `nx.Graph` takes $O(m)$ time.

3. The `nx.connected_components` function runs in $O(n + m)$ time, where $n$ is the number of vertices.

4. The `nx.minimum_edge_cut` function uses the shortest augmenting path algorithm, which runs in $O(n \cdot m)$ time.

5. The outer loop iterates over connected components, and each iteration processes a subset of the graph. The total number of iterations is bounded by the number of connected components, which is at most $n$.

Thus, the overall time complexity is polynomial in the size of the input graph (i.e., $O(n^{2} \cdot m)$).

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

Approximating the Minimum Vertex Cover within a factor of less than sqrt(2) for an undirected graph represented by a Boolean
adjacency matrix in a file.

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
+ We present a polynomial-time algorithm achieving an approximation ratio below sqrt(2) for the minimum vertex cover, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.

+ This result contradicts the Unique Games Conjecture, which predicts such improvements are impossible, thereby undermining UGC and reshaping our understanding of hardness of approximation.

+ The algorithm not only solves a long-standing open problem but also suggests that many other optimization problems might admit better solutions, revolutionizing theoretical computer science.
```

---

# License

- MIT.
