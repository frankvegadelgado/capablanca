# Created on 01/30/2025
# Author: Frank Vega

import scipy.sparse as sparse
import numpy as np
import random
import string
import os
import networkx as nx
from itertools import chain, combinations

def get_file_name(filepath):
    """
    Gets the file name from an absolute path.

    Args:
        filepath: The absolute path to the file.

    Returns:
        The file name, or None if no file is found.
    """

    return os.path.basename(filepath)
    
def get_extension_without_dot(filepath):
    """
    Gets the file extension without the dot from an absolute path.

    Args:
        filepath: The absolute path to the file.

    Returns:
        The file extension without the dot, or None if no extension is found.
    """

    filename = get_file_name(filepath)
    _, ext = os.path.splitext(filename)
    return ext[1:] if ext else None

def has_one_on_diagonal(adjacency_matrix):
    """
    Checks if there is a 1 on the diagonal of a SciPy sparse matrix.

    Args:
      adjacency_matrix: A SciPy sparse matrix (e.g., csc_matrix) representing the adjacency matrix.

    Returns:
        True if there is a 1 on the diagonal, False otherwise.
    """
    diagonal = adjacency_matrix.diagonal()
    return np.any(diagonal == 1)

def is_symmetric(matrix):
    """Checks if a SciPy sparse matrix is symmetric.

    Args:
        matrix: A SciPy sparse matrix.

    Returns:
        bool: True if the matrix is symmetric, False otherwise.
        Raises TypeError: if the input is not a sparse matrix.
    """
    if not sparse.issparse(matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")

    rows, cols = matrix.shape
    if rows != cols:
        return False  # Non-square matrices cannot be symmetric

    # Efficiently check for symmetry
    return (matrix != matrix.T).nnz == 0

def generate_short_hash(length=6):
    """Generates a short random alphanumeric hash string.

    Args:
        length: The desired length of the hash string (default is 6).

    Returns:
        A random alphanumeric string of the specified length.
        Returns None if length is invalid.
    """

    if not isinstance(length, int) or length <= 0:
        print("Error: Length must be a positive integer.")
        return None

    characters = string.ascii_letters + string.digits  # alphanumeric chars
    return ''.join(random.choice(characters) for i in range(length))

def make_symmetric(matrix):
    """Makes an arbitrary sparse matrix symmetric efficiently.

    Args:
        matrix: A SciPy sparse matrix (e.g., csc_matrix, csr_matrix, etc.).

    Returns:
        scipy.sparse.csc_matrix: A symmetric sparse matrix.
    Raises:
        TypeError: if the input is not a sparse matrix.
    """

    if not sparse.issparse(matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")

    rows, cols = matrix.shape
    if rows != cols:
        raise ValueError("Matrix must be square to be made symmetric.")

    # Convert to COO for efficient duplicate handling
    coo = matrix.tocoo()

    # Concatenate row and column indices, and data with their transposes
    row_sym = np.concatenate([coo.row, coo.col])
    col_sym = np.concatenate([coo.col, coo.row])
    data_sym = np.concatenate([coo.data, coo.data])

    # Create the symmetric matrix in CSC format
    symmetric_matrix = sparse.csc_matrix((data_sym, (row_sym, col_sym)), shape=(rows, cols))
    symmetric_matrix.sum_duplicates() #sum the duplicates

    return symmetric_matrix

def random_matrix_tests(matrix_shape, sparsity=0.9):
    """
    Performs random tests on a sparse matrix.

    Args:
        matrix_shape (tuple): Shape of the matrix (rows, columns).
        num_tests (int): Number of random tests to perform.
        sparsity (float): Sparsity of the matrix (0.0 for dense, close to 1.0 for very sparse).

    Returns:
        list: A list containing the results of each test.
        sparse matrix: the sparse matrix that was tested.
    """

    rows, cols = matrix_shape
    size = rows * cols

    # Generate a sparse matrix using random indices and data
    num_elements = int(size * (1 - sparsity))  # Number of non-zero elements
    row_indices = np.random.randint(0, rows, size=num_elements)
    col_indices = np.random.randint(0, cols, size=num_elements)
    data = np.ones(num_elements, dtype=np.int8)

    sparse_matrix = sparse.csc_matrix((data, (row_indices, col_indices)), shape=(rows, cols))

    symmetric_matrix = make_symmetric(sparse_matrix)  

    symmetric_matrix.setdiag(0)

    return symmetric_matrix

def string_result_format(result, count_result=False):
  """
  Returns a string indicating the vertex cover.
  
  Args:
    result: None if the graph is empty, the vertex cover otherwise.
    count_result: Count the number of nodes in the vertex cover (default is False).

  Returns:
    - "Empty Graph" if result is None, "Vertex Cover Found a, b, c, ...." otherwise.
  """
  if result:
    if count_result:
        return f"Vertex Cover Size {len(result)}"
    else:
        formatted_string = f'{", ".join(f"{x}" for x in result)}'
        return f"Vertex Cover Found {formatted_string}"
  else:
     return "Empty Graph"

def println(output, logger, file_logging=False):
    """ Log and Print the Final Output Message """
    if (file_logging):
        logger.info(output)
    print(output)

def sparse_matrix_to_edges(adj_matrix, is_directed=False):
    """
    Converts a SciPy sparse adjacency matrix to a set of edges.

    Args:
        adj_matrix: A SciPy sparse adjacency matrix.
        is_directed: Whether the matrix represents a directed graph (default: False).

    Returns:
        A set of tuples representing the edges.
    """

    edges = set()
    rows, cols = adj_matrix.nonzero()
    if is_directed:
        for i, j in zip(rows, cols):
            edges.add((i, j))
    else:
        for i, j in zip(rows, cols):
            if i <= j: # Avoid duplicates in undirected graphs
                edges.add((i, j))
    return edges

def networkx_to_graph_dict(G):
  """
  Converts a NetworkX graph to a dictionary representation.

  Args:
    G: The NetworkX graph object.

  Returns:
    A dictionary where keys are vertices and values are lists of adjacent vertices.
  """

  graph_dict = {}
  for node in G.nodes:
    graph_dict[node] = list(G.neighbors(node)) 
  return graph_dict


def powerset(iterable):
    """
    Generate all possible subsets of an iterable.
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def is_independent_set(G, subset):
    """
    Checks if a subset of nodes forms an independent set in the graph.
    """
    for u in subset:
        for v in subset:
            if u != v and G.has_edge(u, v):
                return False
    return True

def is_dominating_set(G, subset):
    """
    Checks if a subset of nodes forms a dominating set in the graph.
    """
    for node in G.nodes:
        if node not in subset and not any(G.has_edge(node, neighbor) for neighbor in subset):
            return False
    return True

def find_independent_dominating_set_brute_force(adj_matrix):
    """
    Finds an independent dominating set in a graph represented by a SciPy sparse adjacency matrix using brute force.

    Args:
        adj_matrix: SciPy sparse adjacency matrix of the graph.

    Returns:
        A set of nodes forming an independent dominating set, or None if not found.
    """

    G = nx.from_scipy_sparse_matrix(adj_matrix)
    all_subsets = powerset(G.nodes)

    for subset in all_subsets:
        if is_independent_set(G, subset) and is_dominating_set(G, subset):
            return subset

    return None

def find_independent_dominating_set(adj_matrix):
    """
    Finds an independent dominating set in a graph represented by a SciPy sparse adjacency matrix.

    Args:
        adj_matrix: SciPy sparse adjacency matrix of the graph.

    Returns:
        A set of nodes forming an independent dominating set.
    """

    # Convert adjacency matrix to NetworkX graph
    G = nx.from_scipy_sparse_matrix(adj_matrix)

    # Find a maximal independent set 
    # (Note: This is not guaranteed to be minimum)
    independent_set = nx.maximal_independent_set(G)

    # Check if the independent set is also dominating
    if nx.is_dominating_set(G, independent_set):
        return independent_set
    else:
        return None

def is_vertex_cover(G, subset):
    """
    Checks if a subset of nodes forms a vertex cover set in the graph.
    """
    for u, v in G.edges():
        if u not in subset and v not in subset:
            return False
    return True

def is_vertex_redundant(graph, vertex, vertex_set):
    """
    Check if a vertex does not cover any edge that a set of vertices does not already cover.

    Parameters:
    - graph: A NetworkX graph.
    - vertex: The vertex to check.
    - vertex_set: A set of vertices.

    Returns:
    - True if the vertex does not cover any additional edge, False otherwise.
    """
    # Get all edges covered by the vertex set
    edges_covered_by_set = set()
    for v in vertex_set:
        edges_covered_by_set.update(graph.edges(v))

    # Get all edges covered by the vertex
    edges_covered_by_vertex = set(graph.edges(vertex))

    # Check if the edges covered by the vertex are a subset of the edges covered by the set
    return edges_covered_by_vertex.issubset(edges_covered_by_set)