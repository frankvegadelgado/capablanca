def dimacs(lines):
    """Parses a DIMACS CNF file and returns a list of clauses.

    Args:
        lines: A list of lines from the DIMACS file.

    Returns:
        A list of clauses, where each clause is a list of literals.
    """

    clauses = []
    variable_map = {}
    max_variable = 0

    for line in lines:
        line = line.strip()
        if not line.startswith('c') and not line.startswith('p'):
            clause = [int(literal) for literal in line.split(' ') if literal != '0']
            max_variable = max(max_variable, max(abs(literal) for literal in clause))
            for literal in clause:
                variable = abs(literal)
                if variable not in variable_map:
                    variable_map[variable] = len(variable_map) + 1
            clauses.append(clause)

    return clauses, variable_map, max_variable
    
def read(path, extension):
    lines = []
    if extension == 'cnf':
        file = open(path, 'r')
        lines = file.readlines()    
    return dimacs(lines)