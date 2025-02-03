# Created on 01/30/2025
# Author: Frank Vega

import scipy.sparse as sparse
import itertools
import networkx as nx

from . import utils

def find_vertex_cover(adjacency_matrix):
    """
    Calculates an approximate vertex cover in polynomial time with an approximation ratio of 7/5 for large enough graphs.
    
    Args:
        adjacency_matrix: A SciPy sparse adjacency matrix.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
        Raises ValueError if the input matrix is not square.
        Raises TypeError if the input is not a sparse matrix.
    """
    
    if not sparse.issparse(adjacency_matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")
  
    n = adjacency_matrix.shape[0]
    if adjacency_matrix.shape[0] != adjacency_matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
  
    if n == 0 or adjacency_matrix.nnz == 0:
        return None # Handle empty graph
    
    edges = utils.sparse_matrix_to_edges(adjacency_matrix)
    graph = nx.Graph(edges)
    approximate_vertex_cover = set() 
    components = list(nx.connected_components(graph))
    while components:
        component = components.pop()
        G = graph.subgraph(component).copy() # Important: Create a copy
        if G.number_of_edges() > 0:
            tree = nx.minimum_spanning_tree(G, algorithm="kruskal")
            matching = nx.bipartite.hopcroft_karp_matching(tree)
            vertex_cover = nx.bipartite.to_vertex_cover(tree, matching)
            approximate_vertex_cover.update(vertex_cover) 
            G.remove_nodes_from(vertex_cover)
        
            components.extend(list(nx.connected_components(G)))

    return approximate_vertex_cover

def find_vertex_cover_brute_force(adj_matrix):
    """
    Calculates the exact minimum vertex cover using brute-force (exponential time).

    Args:
        adj_matrix: A SciPy sparse adjacency matrix.

    Returns:
        A set of vertex indices representing the minimum vertex cover, or None if the graph is empty.
        Raises ValueError if the input matrix is not square.
        Raises TypeError if the input is not a sparse matrix.
    """
  
    if not sparse.issparse(adj_matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")
  
    n_vertices = adj_matrix.shape[0]
    if adj_matrix.shape[0] != adj_matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
  
    if n_vertices == 0 or adj_matrix.nnz == 0:
        return None # Handle empty graph

    edges = utils.sparse_matrix_to_edges(adj_matrix)
    graph = nx.Graph()
    graph.add_edges_from(edges)
    
    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for cover_candidate in itertools.combinations(range(n_vertices), k):
            cover_candidate = set(cover_candidate)
            if utils.is_vertex_cover(graph, cover_candidate):
                return cover_candidate
                
    return None



def find_vertex_cover_approximation(adj_matrix):
    """
    Calculates the approximate vertex cover using an approximation (polynomial time).

    Args:
        adj_matrix: A SciPy sparse adjacency matrix.

    Returns:
        A set of vertex indices representing an approximation of the minimum vertex cover, or None if the graph is empty.
        Raises ValueError if the input matrix is not square.
        Raises TypeError if the input is not a sparse matrix.
    """
    
    if not sparse.issparse(adj_matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")
  
    n_vertices = adj_matrix.shape[0]
    if adj_matrix.shape[0] != adj_matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
  
    if n_vertices == 0 or adj_matrix.nnz == 0:
        return None # Handle empty graph

    edges = utils.sparse_matrix_to_edges(adj_matrix)
    graph = nx.Graph()
    graph.add_edges_from(edges)
    #networkx doesn't have a guaranteed minimum vertex cover function, so we use approximation
    vertex_cover = nx.approximation.vertex_cover.min_weighted_vertex_cover(graph)
    return vertex_cover