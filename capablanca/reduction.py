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
                unique_clause + [-A],
                unique_clause + [B],
                unique_clause + [-B]
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

def reduce_cnf_to_3sat(clauses, max_variable):
    """Reduces a CNF formula to a 3SAT instance.

    Args:
        clauses: A list of clauses in CNF form.
        max_variable: The maximum variable in the CNF formula.
    
    Returns:
        A list of 3CNF clauses.
    """

    # Convert the CNF formula to 3SAT
    three_sat_clauses, _ = reduce_sat_to_3sat(clauses, max_variable)

    return three_sat_clauses