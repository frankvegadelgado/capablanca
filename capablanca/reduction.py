from . import utils
    
def reduce_sat_to_3sat(clauses, max_variable):
    """
    Converts a formula in SAT format to a 3CNF formula.

    Args:
        clauses: A list of clauses, where each clause is a list of literals.
        max_variable: The maximum variable in the input formula.

    Returns:
        A tuple (new_clauses, new_max_variable), where:
            - new_clauses: A list of 3CNF clauses.
            - new_max_variable: The maximum variable in the new 3CNF formula.
    """
  
    new_clauses = []
    next_variable = max_variable + 1
    A, B = next_variable, next_variable + 1 # Create Global Variables
    next_variable += 2
    
    for literals in clauses:
        clause = list(set(literals)) # Ensure clauses with distinct literals
        if len(clause) == 1: # Unit clause
            literal = clause[0]
            new_clauses.extend([[literal, A, B], 
                          [literal, -A, B], 
                          [literal, A, -B], 
                          [literal, -A, -B]])
        elif len(clause) == 2: # 2CNF clause
            new_clauses.extend([clause + [A], 
                          clause + [-A], 
                          clause + [B], 
                          clause + [-B]])
        elif len(clause) > 3: # kCNF clause with k > 3
            while len(clause) > 3:
                D = next_variable
                new_clauses.append(clause[:2] + [D])
                clause = [-D] + clause[2:]
                next_variable += 1
            new_clauses.append(clause)
        else: # 3CNF clause
            new_clauses.append(clause)

    return new_clauses, next_variable - 1    

def reduce_3sat_to_1_in_3_3msat(clauses, max_variable):
    """
    Converts a 3SAT formula to a monotone 1-IN-3-3SAT instance.

    Args:
        clauses: A list of 3CNF clauses.
        max_variable: The maximum variable in the input formula.

    Returns: A tuple (new_clauses, new_max_variable), where:
            - new_clauses: A list of monotone 1-IN-3-3SAT clauses.
            - new_max_variable: The maximum variable in the new 3CNF formula.
    """

    new_clauses = []
    next_variable = 2 * max_variable + 2
    
    variables = utils.convert_to_absolute_value_set(clauses) # Set of all variables

    for variable in variables: # Keep consistency between x and ¬x
        positive_literal = utils.double(variable) # Map variable to 2 * variable
        negative_literal = utils.double(-variable)  # Map =variable to 2 * variable + 1

        new_var = next_variable
        new_clauses.extend([[positive_literal, negative_literal, new_var],
                         [positive_literal, negative_literal, new_var + 1],
                         [new_var, new_var + 1, new_var + 2]])
        next_variable += 3
    
    for clause in clauses: # Classic reduction from 3SAT to 1-IN-3-3SAT 
        # We map literals to positive variables
        x, y, z = utils.double(-clause[0]), utils.double(clause[1]), utils.double(-clause[2])
        # Auxiliary variables
        a, b, d, e = next_variable, next_variable + 1, next_variable + 2, next_variable + 3 
        # monotone 1-IN-3-3SAT clauses
        new_clauses.extend([[x, a, b], [y, b, d], [z, d, e]])
        next_variable += 4
    
    return new_clauses, next_variable - 1    


def reduce_1_in_3_3msat_to_unknown(clauses, max_variable):
    """
    Converts a 3SAT formula to a Unknown instance.

    Args:
        clauses: A list of 3CNF clauses.
        max_variable: The maximum variable in the input formula.

    Returns: A tuple (new_clauses), where:
            - new_clauses: A list of Unknown clauses.
    """

    new_clauses = []
    next_variable = max_variable + 1
    # Dictionary of variable pairs
    pairs_dict = {}

    for clause in clauses:
        # Sort monotone clause in ascending order
        sorted_clause = list(sorted(clause))
        # Sorted variables
        x, y, z = sorted_clause[0], sorted_clause[1], sorted_clause[2]
        # Sorted Pairs such that (a, b) = (min(a, b), max(a, b))
        x_y, y_x, x_z = (x, y), (y, z), (x, z)
        pairs_list = [x_y, y_x, x_z]
        for pair in pairs_list: # Register each new pair
            if pair not in pairs_dict:
                pairs_dict[pair] = next_variable
                next_variable += 1
        # Unknown instance        
        new_clauses.extend([[x, y, z]])        
    
    return new_clauses    

def reduce_sat(clauses, max_variable, brute_force=False):
    """
    Reduces a CNF formula to an 3SAT instance.

    Args:
        clauses: A list of clauses in CNF form.
        max_variable: The maximum variable.
        brute_force: A boolean indicating whether to use brute force reduction.

    Returns: A tuple (new_clauses, pure_literals), where:
            - new_clauses: A list of 3CNF clauses
            - pure_literals: Literals determined to be always true after simplification.
    """

    # Convert the CNF formula to 3SAT
    new_clauses, next_variable = reduce_sat_to_3sat(clauses, max_variable)
    
    if brute_force:

        # Convert the 3SAT formula to mock 1-IN-3-3SAT
    
        new_clauses, next_variable = utils.reduce_3sat_to_mock_1_in_3_3msat(new_clauses, next_variable)

    else: 
        # Convert the 3SAT formula to monotone 1-IN-3-3SAT
        
        new_clauses, next_variable = reduce_3sat_to_1_in_3_3msat(new_clauses, next_variable)
    
        # Convert the monotone 1-IN-3-3SAT formula to Unknown

        new_clauses = reduce_1_in_3_3msat_to_unknown(new_clauses, next_variable)
        
    return new_clauses