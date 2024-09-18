#                          SAT Solver
#                          Frank Vega
#                     September 18, 2024

import argparse
import sys
import networkx 
import time
s=0
maximum=0
log = False
timed = False
started = 0.0

def logging(message):
    if log:
        print(message)

def FSAT_to_3SAT(clauses):
    global s, maximum
    a = maximum + 1
    b = maximum + 2
    s = maximum + 3
    new_clauses = []
    for l in clauses:
        C = list(set(l))
        if len(C) == 1:
            new_clauses.append([C[0], a, b])
            new_clauses.append([C[0], -a, b])
            new_clauses.append([C[0], a, -b])
            new_clauses.append([C[0], -a, -b])
        elif len(C) == 2:
            new_clauses.append([C[0], C[1], b])
            new_clauses.append([C[0], C[1], -b])
        elif len(C) == 3:
            new_clauses.append(C)
        elif len(C) > 3:
            B = C
            while True:
                A = B[:2]
                B = B[2:]
                A.append(s)
                B.append(-s)
                s += 1
                new_clauses.append(A)
                if len(B) == 3:
                    break
            new_clauses.append(B)
    return new_clauses 

def F3SAT_to_CLIQUE(clauses):
    global s
    
    s = 0
    
    edges = []
    
    k = len(clauses)
    
    chain = {}
    
    for i in range(k):
        x, y, z = clauses[i][0], clauses[i][1], clauses[i][2]
        a, b, c = s,s+1,s+2
        chain[(x, i)] = a
        chain[(y, i)] = b
        chain[(z, i)] = c
        
        s += 3
    
    for i in range(k):
        clause_i = clauses[i]
        for j in range(i + 1, k):
            clause_j = clauses[j]
            for x in clause_i:
                for y in clause_j:
                    if x != -y:
                        edges.append((chain[(x, i)], chain[(y, j)]))
    
    graph = networkx.Graph()
    graph.add_edges_from(edges)  
    
    return (graph, k)

def FCLIQUE_to_CLOSURE(graph, k):
    global s
    
    n = len(graph.nodes())
    
    m = len(graph.edges())
    
    newK = k + 2 * k * (n - k)
    
    edges = []
    
    for i in range(n):
        u = i
        for j in range(i+1, n):
            v = j
            if (u not in graph[v] and v not in graph[u]):
                for ramp in range(k):
                    edges.append((u, s))
                    edges.append((v, s+1))
                    s += 2    
    
    G = networkx.DiGraph()
    G.add_edges_from(edges)  
    
    return (G, newK)
    
def FCLOSURE_to_MX2SAT(graph, k):
    global s
    
    source_edges = graph.edges()
    
    m = len(source_edges)
    
    newK = k + m
    
    edges = []
    
    for u, v in source_edges:
        edges.append((u, s))
        edges.append((v, s))
        edges.append((s, s+1))
        s += 2    

    G = networkx.Graph()
    G.add_edges_from(edges)  
    
    return (G, newK)
    
def polynomial_time_reduction(source):
    clauses = FSAT_to_3SAT(source)
    graph, k = F3SAT_to_CLIQUE(clauses)
    graph, k = FCLIQUE_to_CLOSURE(graph, k)
    graph, k = FCLOSURE_to_MX2SAT(graph, k)
    
    return (graph, k)
   
def solution(graph):
    
    solution = 0
    
    if networkx.algorithms.bipartite.is_bipartite(graph):
        components = networkx.connected_components(graph)
        for component in components:
            G = networkx.induced_subgraph(graph, component)
            matching = networkx.bipartite.maximum_matching(G)
            vertex_cover = networkx.bipartite.to_vertex_cover(G, matching)
            independent_set = set(G) - vertex_cover
            solution += len(independent_set)
    else:
        return None

    return solution
            
        
def parse_dimacs(asserts):
    global maximum
    mapped = {}
    result = []
    for strvar in asserts:
        line = strvar.strip()
        if not line.startswith('p') and not line.startswith('c'):
            expr = line.split(" ")
            expr = expr[:-1]
            l = []
            for t in expr:
                v = int(t)
                l.append(v)
                value = abs(v)
                if value not in mapped:
                    mapped[value] = True
                    maximum = value if (maximum < value) else maximum
            result.append(list(set(l)))        
    return result   
                       
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve an NP-complete problem from a DIMACS file.')
    parser.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    
    args = parser.parse_args()

    log = args.verbose
    timed = args.timer
    
    #Read and parse a dimacs file
    
    logging("Pre-processing started")
    if timed:
        started = time.time()
    file = open(args.inputFile, 'r')
    #Format from dimacs
    asserts = file.readlines()    
    source = parse_dimacs(asserts)
    if timed:
        logging(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Pre-processing done")
    
    logging("Starting the polynomial time reduction")
    if timed:
        started = time.time()
    
    # Polynomial Time Reduction
    graph, k = polynomial_time_reduction(source)
    
    if timed:
        logging(f"Polynomial time reduction done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Polynomial time reduction done")
    
    logging("Start searching the solution")
    if timed:
        started = time.time()
       
    # Solving in Polynomial Time
    answer = solution(graph)
    if timed:
        logging(f"Searching the solution done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Searching the solution done")
    
    # Output the solution
    if answer is None:
        print("s UNKNOWN")
    else:
        if answer >= k:
            print("s SATISFIABLE")
        else:
            print("s UNSATISFIABLE")