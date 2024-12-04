#                          SAT Solver (Brute Force)
#                          Frank Vega
#                      December 3rd, 2024
#     We use Z3 that is a theorem prover from Microsoft Research.

import argparse
import sys
import networkx
import time
import z3
z3.set_option(model=True)
z3.set_param("parallel.enable", False)
log = False
timed = False
started = 0.0

# Write to the Standard Output
def logging(message):
    """Logs a message to the console if the global `log` variable is True.

    Args:
        message: The message to be logged.
    """

    if log:
        # Using the built-in `print` function is fine for simple logging,
        # but for more advanced logging, consider using the `logging` module.
        print(message)
        
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
    new_clauses = [[a, b, c]]    
    next_variable += 3
    
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

    

def solve_formula(solver, variable_map, tautology_set, initial_variable_map):
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
       
def parse_dimacs(lines):
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
                       
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.')
    parser.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    
    args = parser.parse_args()

    log = args.verbose
    timed = args.timer
    
    # Read and parse a dimacs file
    
    logging("Pre-processing started")
    if timed:
        started = time.time()
    
    # Format from dimacs
    file = open(args.inputFile, 'r')
    lines = file.readlines()    
    formula, initial_variable_map, max_variable = parse_dimacs(lines)
    
    if timed:
        logging(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Pre-processing done")
    
    logging("Starting the polynomial time reduction")
    if timed:
        started = time.time()
    
    # Polynomial Time Reduction
    clauses, tautology_set, variable_map, next_variable = reduce_to_3cnf(formula, initial_variable_map, max_variable)
    
    if timed:
        logging(f"Polynomial time reduction done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Polynomial time reduction done")
    
    logging("Starting the data structure creation")
    if timed:
        started = time.time()
    
    # Creating the data structure
    solver = build(clauses, variable_map)
    
    if timed:
        logging(f"Data structure creation done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Data structure creation")
    
    
    logging("Start solving the problem")
    if timed:
        started = time.time()
       
    # Solving in Polynomial Time
    answer = solve_formula(solver, variable_map, tautology_set, initial_variable_map)
    
    if timed:
        logging(f"Solving the problem done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Solving the problem done")
    
    # Output the solution
    logging("Starting to check the solution")
    if timed:
        started = time.time()

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
    
    if timed:
        logging(f"Check the solution done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logging("Check the solution done")

    if Satisfiability:
        print("s SATISFIABLE")
        sys.stdout.write("v ")
        for x in assigned_literals:
            sys.stdout.write("%s " % x)
        print("0")
    else:
        print("s UNSATISFIABLE")    