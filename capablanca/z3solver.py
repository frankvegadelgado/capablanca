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
        A Z3 solver instance (3SAT Solver).
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
