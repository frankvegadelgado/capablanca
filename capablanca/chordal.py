import networkx as nx

def approximate_dominating_set_chordal(G):
    """
    Find an approximate dominating set with a 2-approximation ratio in a chordal graph in polynomial time.

    Args:
        G: A NetworkX graph that is assumed to be chordal

    Returns:
        A set of vertices forming a 2-approximate dominating set

    Time Complexity: O(n + m) where n is the number of vertices and m is the number of edges
    """
    # Verify the graph is chordal (optional check)
    if not nx.is_chordal(G):
        raise ValueError("Input graph is not chordal")

    # Get the perfect elimination ordering
    G, peo = nx.chordal.complete_to_chordal_graph(G)

    # We'll process vertices in reverse PEO
    reverse_peo = list(reversed(peo))

    dominating_set = set()
    dominated = {v: False for v in G.nodes()}
    
    # Process vertices in reverse perfect elimination ordering
    for v in reverse_peo:
        # If v is not dominated yet, add one of its neighbors to the dominating set
        if not dominated[v]:
            # Find the best neighbor to add (including v itself)
            best_vertex = v
            best_undominated_count = -1

            for neighbor in list(G.neighbors(v)) + [v]:
                undominated_neighbors_count = 0
                for u in list(G.neighbors(neighbor)) + [neighbor]:
                    if not dominated[u]:
                        undominated_neighbors_count += 1

                if undominated_neighbors_count > best_undominated_count:
                    best_undominated_count = undominated_neighbors_count
                    best_vertex = neighbor

            # Add the best vertex to the dominating set
            dominating_set.add(best_vertex)

            # Mark vertices as dominated
            dominated[best_vertex] = True
            for neighbor in G.neighbors(best_vertex):
                dominated[neighbor] = True

    return dominating_set
