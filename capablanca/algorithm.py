# Created on 03/25/2025
# Author: Frank Vega

import itertools
import networkx as nx
from . import chordal

def find_dominating_set(graph):
    """
    Find a 2-approximate dominating set with a 2-approximation ratio for an undirected graph by transforming it into a chordal graph.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the 2-approximate dominating set.
             Returns an empty set if the graph is empty or has no edges.
    """
    # Validate input graph
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")

    # Handle empty graph or graph with no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()

    # Include isolated nodes in the dominating set and remove them from the graph
    optimal_dominating_set = set(nx.isolates(graph))
    graph.remove_nodes_from(optimal_dominating_set)

    # If the graph becomes empty after removing isolated nodes, return the set of isolated nodes
    if graph.number_of_nodes() == 0:
        return optimal_dominating_set

    for component in nx.connected_components(graph):
    
        # Subgraph for the connected component
        subgraph = graph.subgraph(component)
    
        # Create a new graph to transform the original into a chordal graph structure
        chordal_graph = nx.Graph()
        
        # Add edges to create a chordal structure
        # This ensures the dominating set in the chordal graph corresponds to one in the original subgraph
        for i in subgraph.nodes():
            chordal_graph.add_edge((i, 0), (i, 1))
            for j in subgraph.neighbors(i):
                    # Create tuple nodes in the chordal graph
                    chordal_graph.add_edge((i, 0), (j, 1))
        
        # Add edges to ensure chordality by forming a clique among (i, 0) nodes
        for i in subgraph.nodes():
            for j in subgraph.nodes():
                if i < j:
                    chordal_graph.add_edge((i, 0), (j, 0))

        # Compute the approximate dominating set in the transformed chordal graph
        tuple_nodes = chordal.approximate_dominating_set_chordal(chordal_graph)

        # Extract original nodes from the tuple nodes and update the dominating set
        optimal_dominating_set.update({tuple_node[0] for tuple_node in tuple_nodes})

    return optimal_dominating_set


def find_dominating_set_brute_force(graph):
    """
    Computes an exact minimum dominating set in exponential time.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the exact dominating set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    n_vertices = len(graph.nodes())

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for candidate in itertools.combinations(graph.nodes(), k):
            cover_candidate = set(candidate)
            if nx.dominating.is_dominating_set(graph, cover_candidate):
                return cover_candidate
                
    return None



def find_dominating_set_approximation(graph):
    """
    Find an approximate dominating set in polynomial time with a logarithmic approximation ratio for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate dominating set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    #networkx doesn't have a guaranteed minimum dominating set function, so we use approximation
    dominating_set = nx.approximation.dominating_set.min_weighted_dominating_set(graph)
    return dominating_set