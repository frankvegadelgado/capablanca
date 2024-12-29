#     We use Z3 that is a theorem prover from Microsoft Research.

import z3
z3.set_option(model=True)
z3.set_param("parallel.enable", False)

from . import utils

def build(clauses):
    """Builds a Z3 solver instance with constraints corresponding to the given clauses.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.

    Returns:
        A Z3 solver instance.
    """
    
    variables = utils.convert_to_absolute_value_set(clauses) # Set of all variables

    s = z3.Solver()
    smt2 = [('(declare-fun |%s| () Bool)' % variable) for variable in variables]
    for clause in clauses:
        x = '(not |%s|)' % (-clause[0]) if (clause[0] < 0) else '|%s|' % clause[0]
        y = '(not |%s|)' % (-clause[1]) if (clause[1] < 0) else '|%s|' % clause[1]
        z = '(not |%s|)' % (-clause[2]) if (clause[2] < 0) else '|%s|' % clause[2]
        smt2.append('(assert (or %s (or %s %s)))' % (x, y, z))
    smt2.append('(check-sat)')
    s.from_string("%s" % '\n'.join(smt2))
    
    return s

    

def solve(solver, formula, max_variable):
    """Solves the formula represented by the Z3 solver and return the result.

    Args:
        solver: A Z3 solver instance containing the formula.
        formula: The original SAT formula.
        max_variable: The maximum variable in the orignal formula.

    Returns:
    A tuple (satisfiability, solution) where:
        - satisfiability: True if the formula is satisfiable, False otherwise.
        - solution: A satisfying truth assignment if satisfiable, None otherwise.
    """
    
    answer = solver.check()
    if answer == z3.unsat:
        return False, None
    elif answer == z3.sat:
        solution = set()
        visited = {}
        model = solver.model()
        for d in model.decls():
            literal = int(d.name())
            variable = literal // 2
            if variable <= max_variable:
                value = ('%s' % model[d])
                visited[variable] = True
                literal = variable if (literal % 2 == 0) else -variable
                if value == 'False': 
                    solution.add(-literal)
                else:
                    solution.add(literal)

        variables = utils.convert_to_absolute_value_set(formula) # Set of all variables
            
        for z in variables:
            if z <= max_variable:
                if z not in visited and -z not in visited:
                    solution.add(z)
    
        return True, solution 
    else: 
        return None, None 
    
    
    