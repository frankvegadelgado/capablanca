#                          SAT Solver
#                          Frank Vega
#                      December 3rd, 2024
#     We use Z3 that is a theorem prover from Microsoft Research.

import z3
z3.set_option(model=True)
z3.set_param("parallel.enable", False)

def build(clauses, variable_map):
    """Builds a Z3 solver instance with constraints corresponding to the given clauses.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.

    Returns:
        A Z3 solver instance.
    """
    
    s = z3.Solver()
    smt2 = [ ('(declare-fun |%s| () Bool)' % (i+1)) for i in range(len(variable_map)) ]
    for clause in clauses:
        x = '(not |%s|)' % (variable_map[-clause[0]]) if (clause[0] < 0) else '|%s|' % variable_map[clause[0]]
        y = '(not |%s|)' % (variable_map[-clause[1]]) if (clause[1] < 0) else '|%s|' % variable_map[clause[1]]
        z = '(not |%s|)' % (variable_map[-clause[2]]) if (clause[2] < 0) else '|%s|' % variable_map[clause[2]]
        smt2.append('(assert (or %s (or %s %s)))' % (x, y, z))
    smt2.append('(check-sat)')
    s.from_string("%s" % '\n'.join(smt2))
    
    return s

    

def solve_formula(solver, variable_map, tautology_set, initial_variable_map, max_variable):
    """Solves the formula represented by the Z3 solver and prints the result.

    Args:
        solver: A Z3 solver instance containing the formula.
    """
    
    result = solver.check()
    solution = [] 
    visited = {}
    
    for z in tautology_set:
        solution.append(z)
        visited[z] = True  
    
    if result == z3.sat:
    
        model = solver.model()
        inverse_variable_map = {variable_map[key]: key for key in variable_map}  # Inverted variable map
        for d in model.decls():
            v = int(d.name())
            if inverse_variable_map[v] <= max_variable:
                value = ('%s' % model[d])
                visited[inverse_variable_map[v]] = True
                if value == 'False': 
                    solution.append(-inverse_variable_map[v])
                else:
                    solution.append(inverse_variable_map[v])
    
    for z in initial_variable_map:
        if z <= max_variable:
            if z not in visited and -z not in visited:
                solution.append(z)
    
    return solution