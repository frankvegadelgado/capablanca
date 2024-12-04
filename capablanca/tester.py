def check(formula, answer, initial_variable_map):
    assigned_literals = set()
    negate_assigned_literals = set()
    for literal in initial_variable_map:
        assigned_literals.add(literal if literal in answer else -literal)
        negate_assigned_literals.add(-literal if literal in answer else literal)
    
    Satisfiability = True        
    # Check if any clause is unsatisfied
    for clause in formula:
        if not any(literal in assigned_literals for literal in clause):
            Satisfiability = False
            break  # Found an unsatisfied clause    
    
    if Satisfiability:
        return Satisfiability, assigned_literals
    
    Satisfiability = True        
    # Check if any clause is unsatisfied
    for clause in formula:
        if not any(literal in negate_assigned_literals for literal in clause):
            Satisfiability = False
            break  # Found an unsatisfied clause     
    
    if Satisfiability:
        return Satisfiability, negate_assigned_literals
    else:
        return False, set()