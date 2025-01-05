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
        A Z3 solver instance (Feasible SAT Solver).
    """
    
    variables = utils.convert_to_absolute_value_set(clauses) # Set of all variables

    s = z3.Solver()
    smt2 = [('(declare-fun |%s| () Bool)' % variable) for variable in variables]

    for original_clause in clauses:
        negated_literals = []
        set_clause = set(original_clause)
        clause = list(set_clause)
        tautology = False
        for x in clause:
            if -x not in set_clause:
                negated_literals.append('|%s|' % -x if (x < 0) else '(not |%s|)' % x)
            else:
                tautology = True
                break
        if tautology:
            continue
        else:        
            smt2.append('(assert (ite (and %s) false true))' % ' '.join(negated_literals))

    smt2.append('(check-sat)')
    s.from_string("%s" % '\n'.join(smt2))
    
    return s

def solve(solver, formula, max_variable):
    """Solves feasible the formula represented by the Z3 solver and return the result.

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
            variable = abs(literal)
            if variable <= max_variable:
                value = ('%s' % model[d])
                visited[variable] = True
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