import networkx as nx

from . import utils

def reduce_sat_to_3sat(clauses, max_variable):
    """Converts a formula in SAT format to a 3CNF formula.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.
        max_variable: The maximum variable in the input formula.

    Returns:
        A tuple (three_sat_clauses, new_max_variable), where:
            - three_sat_clauses: A list of 3CNF clauses.
            - new_max_variable: The maximum variable in the new 3CNF formula.
    """

    three_sat_clauses = []
    next_variable = max_variable + 1
    A, B = next_variable, next_variable + 1 # Global Variables
    next_variable += 2

    for clause in clauses:
        # Remove duplicate literals within a clause for efficiency and correctness.
        unique_clause = list(set(clause))

        clause_len = len(unique_clause)

        if clause_len == 1:  # Unit clause
            three_sat_clauses.extend([
                [unique_clause[0], A, B],
                [unique_clause[0], -A, B],
                [unique_clause[0], A, -B],
                [unique_clause[0], -A, -B]
            ])
        elif clause_len == 2:  # 2CNF clause
            three_sat_clauses.extend([
                unique_clause + [A],
                unique_clause + [-A]
            ])
        elif clause_len > 3:  # kCNF clause with k > 3
            current_clause = unique_clause
            while len(current_clause) > 3:
                D = next_variable
                three_sat_clauses.append(current_clause[:2] + [D])
                current_clause = [-D] + current_clause[2:]
                next_variable += 1
            three_sat_clauses.append(current_clause)
        else:  # 3CNF clause
            three_sat_clauses.append(unique_clause)

    return three_sat_clauses, next_variable - 1

def reduce_3sat_to_nae_3sat(clauses, max_variable):
    """
    Converts a 3CNF formula to a NAE-3SAT instance.

    Args:
        clauses: A list of 3CNF clauses.
        variable_map: A dictionary mapping variables to their indices.
        max_variable: The maximum variable index in the input formula.

    Returns:
        A tuple (new_clauses, new_variable_map, new_max_variable), where:
        - new_clauses: A list of NAE-3SAT clauses.
        - new_max_variable: The maximum variable index in the new NAE-3SAT formula.
    """

    new_clauses = []
    next_variable = max_variable + 1
    pivot = next_variable 
    next_variable += 1
        
    for clause in clauses:
        new_var = next_variable
        new_clauses.extend([[clause[0], clause[1], new_var],
                         [clause[2], -new_var, pivot]])
        next_variable += 1

    return new_clauses, next_variable - 1  
    
def double(literal):
    """
    Maps a literal value to its absolute double value.

    Args:
        literal: The literal to be mapped.
        
    Returns: 
        The duplicated mapped literal.
    """

    return 2 * abs(literal) + (1 if literal < 0 else 0)

def reduce_nae_3sat_to_nae_3msat(clauses, max_variable):
    """
    Converts a NAE-3SAT formula to a NAE-3MSAT instance.

    Args:
        clauses: A list of NAE-3SAT clauses.
        max_variable: The maximum variable index in the input formula.

    Returns: A tuple (new_clauses, new_max_variable), where:
            - new_clauses: A list of monotone NAE-3SAT clauses.
            - new_max_variable: The maximum variable index in the new NAE-3MSAT formula.
    """

    new_clauses = []
    next_variable = 2 * max_variable + 2
    variables = utils.convert_to_absolute_value_set(clauses) # Set of all variables

    for variable in variables:
        positive_literal = double(variable)
        negative_literal = double(-variable)

        new_var = next_variable
        new_clauses.extend([[positive_literal, negative_literal, new_var],
                         [positive_literal, negative_literal, new_var + 1],
                         [positive_literal, negative_literal, new_var + 2],
                         [new_var, new_var + 1, new_var + 2]])
        next_variable += 3
    
    for clause in clauses:
        x, y, z = double(clause[0]), double(clause[1]), double(clause[2])
        new_clauses.append([x, y, z])
    
    return new_clauses, next_variable - 1    
    
def reduce_nae_3msat_to_2mxsat(clauses, max_variable):   
    """
    Converts a NAE-3MSAT formula to a 3MSC instance.

    Args:
        clauses: A list of monotone NAE-3MSAT clauses.
        max_variable: The maximum variable index in the input formula.
    
    Returns: A tuple (new_clauses, new_max_variable), where:
            - new_clauses: A list of xor clauses in 2CNF.
            - new_max_variable: The maximum variable index in the new NAE-3MSAT formula.
    """

    
    new_clauses = []
    next_variable = max_variable + 1
    
    for clause in clauses:
        x, y, z = clause[0], clause[1], clause[2]
        a, b, d = next_variable, next_variable + 1, next_variable + 2
        new_clauses.extend([[a, b], [b, d], [a, d], [a, x], [b, y], [d, z]])
        next_variable += 3
    
    return new_clauses, next_variable - 1    
    
    
def reduce_2mxsat_to_3xsp(clauses, max_variable):
    """
    Converts a 2MXSAT formula to a 3XSP instance.

    Args:
        clauses: A list of xor clauses in 2CNF.
        max_variable: The maximum variable index in the input formula.
    
    Returns: A tuple (triples, new_max_variable), where:
            - sets: A list of 3-element sets.
    """

    sets = []
    clause_map = {}
    next_variable = max_variable + 1
    size = len(clauses) 
  
    for i in range(size):
        clause = clauses[i]
        for variable in clause:
            if (variable, i) not in clause_map:
                start, u, v = next_variable, next_variable + 1, next_variable + 2
                original = u
                clause_map[(variable, i)] = start
                variable_sets = [frozenset({start, v, u})]
                end = v
                next_variable += 3
                for j in range(i+1, size):
                    if j < size and variable in clauses[j]:
                        u, v = next_variable, next_variable + 1
                        variable_sets.append(frozenset({-start, end, u}))
                        start = next_variable + 2
                        clause_map[(variable, j)] = start
                        variable_sets.append(frozenset({start, v, u}))
                        end = v
                        next_variable += 3         
                variable_sets.append(frozenset({-start, end, original}))
                sets.extend(variable_sets)
                

    for i in range(size):
        clause = clauses[i]
        x, y = clause_map[(clause[0], i)], clause_map[(clause[1], i)]
        a, b, d, e = next_variable, next_variable + 1, next_variable + 2, next_variable + 3
        clause_sets = [frozenset({x, b, a}), 
                       frozenset({y, b, d}), 
                       frozenset({-y, e, d}), 
                       frozenset({-x, e, a})]
        sets.extend(clause_sets)
        next_variable += 4
        
    return sets

def reduce_3xsp_to_2xhs(sets_3xsp):
    """Reduces 3XSP sets to a 2XHS instance.

    Args:
        sets_3xsp: A list of 3-element sets.
    
    Returns: 
        - A line graph.
    """

    G = nx.Graph()
    for key1, subset1 in enumerate(sets_3xsp):
        for key2, subset2 in enumerate(sets_3xsp):
            if key1 < key2 and subset1.intersection(subset2):
                G.add_edge(key1, key2)

    return G    


def reduce_cnf_to_2xhs(clauses, max_variable):
    """Reduces a CNF formula to a 2XHS instance.

    Args:
        clauses: A list of clauses in CNF form.
        max_variable: The maximum variable in the CNF formula.
    
    Returns: A tuple (G, k), where:
        - G: A line graph.
        - k: The target.
    """

    # Convert the simplified CNF formula to 3SAT
    cnf_3sat_clauses, next_variable = reduce_sat_to_3sat(clauses, max_variable)
    
    # Convert the 3SAT formula to NAE-3SAT
    nae_3sat_clauses, next_variable = reduce_3sat_to_nae_3sat(cnf_3sat_clauses, next_variable)
    
    # Convert the NAE-3SAT formula to monotone NAE-3SAT
    nae_3msat_clauses, next_variable = reduce_nae_3sat_to_nae_3msat(nae_3sat_clauses, next_variable)
    
    # Convert the monotone NAE-3SAT formula to 2MXSAT
    mxsat_clauses, next_variable = reduce_nae_3msat_to_2mxsat(nae_3msat_clauses, next_variable)
    
    # Convert a 2MXSAT to a 3XSP sets
    sets_3xsp = reduce_2mxsat_to_3xsp(mxsat_clauses, next_variable)
    
    # Convert a 3XSP to a line graph that represents the 2XHS sets
    G = reduce_3xsp_to_2xhs(sets_3xsp)
    
    return G, 3 * len(mxsat_clauses) + 5 * len(mxsat_clauses) // 6  