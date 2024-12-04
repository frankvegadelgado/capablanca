def simplify(clauses, map_variable):
    """Simplifies a set of SAT clauses.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.

    Returns:
        A simplified list of clauses.
    """
    
    simplified_clauses = []
    variables_seen = set()

    for clause in clauses:
        # Early termination if clause is unsatisfiable
        if any(literal in clause and -literal in clause for literal in clause):
            continue

        simplified_clauses.append(clause)
        for literal in clause:
            variables_seen.add(literal)
    
    # Identify tautologies and pure literals
    tautologies = []
    pure_literals = []
    for variable in map_variable:
        if variable in variables_seen and -variable not in variables_seen:
            pure_literals.append(variable)
        elif -variable in variables_seen and variable not in variables_seen:
            pure_literals.append(-variable)
        elif variable not in variables_seen and -variable not in variables_seen:
            tautologies.append(variable)
    
    variable_map = {}
    new_clauses = []
    # Remove tautologies and propagate pure literals
    for clause in simplified_clauses:
        if not any(literal in clause for literal in tautologies):
            # Remove pure literals from the clause
            clause = [literal for literal in clause if literal not in pure_literals and -literal not in pure_literals]
            if clause:  # Non-empty clause after pure literal elimination
                new_clauses.append(clause)
                for literal in clause:
                    variable = abs(literal)
                    if variable not in variable_map:
                        variable_map[variable] = len(variable_map) + 1
    
    tautology_set = set(tautologies + pure_literals)
    
    return new_clauses, tautology_set, variable_map
    
def fsat_to_3sat(clauses, map_variable, max_variable):
    """Converts a formula in FSAT format to a 3-CNF formula.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.

    Returns:
        A list of 3-CNF clauses.
    """

    new_clauses = []
    variable_map = map_variable
    next_variable = max_variable + 1
    a, b, c = next_variable, next_variable + 1, next_variable + 2
    variable_map[a] = len(variable_map) + 1
    variable_map[b] = len(variable_map) + 1
    variable_map[c] = len(variable_map) + 1
    new_clauses = [[a, b, c]] if (len(clauses) > 0) else []
    next_variable += 3 if (len(clauses) > 0) else next_variable
    
    for clause in clauses:
        # Handle clauses of different lengths
        if len(clause) == 1:
            # Introduce two new variables
            new_clauses.extend([[clause[0], a, b],
                                [clause[0], -a, b],
                                [clause[0], a, -b],
                                [clause[0], -a, -b]])
        elif len(clause) == 2:
            # Introduce one new variable
            new_clauses.extend([[clause[0], clause[1], b],
                                [clause[0], clause[1], -b]])
        elif len(clause) == 3:
            new_clauses.append(clause)
        else:
            # Break down larger clauses into 3-CNF clauses
            while len(clause) > 3:
                d = next_variable
                new_clauses.append(clause[:2] + [d])
                clause = [-d] + clause[2:]
                next_variable += 1
                variable_map[d] = len(variable_map) + 1
            new_clauses.append(clause)
    
    return new_clauses, variable_map, next_variable
    
def reduce_to_3cnf(clauses, map_variable, max_variable):
    """Reduces a given set of clauses to a 3-CNF formula.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.

    Returns:
        A list of 3-CNF clauses.
    """

    # Simplify the input clauses
    simplified_clauses, tautology_set, variable_map = simplify(clauses, map_variable)
    
    # Convert the simplified clauses to 3-CNF format
    cnf_clauses, variable_map, next_variable = fsat_to_3sat(simplified_clauses, variable_map, max_variable)

    return cnf_clauses, tautology_set, variable_map, next_variable