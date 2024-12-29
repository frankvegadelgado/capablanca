import os

def get_extension_without_dot(filepath):
    """
    Gets the file extension without the dot from an absolute path.

    Args:
        filepath: The absolute path to the file.

    Returns:
        The file extension without the dot, or None if no extension is found.
    """

    filename = os.path.basename(filepath)
    _, ext = os.path.splitext(filename)
    return ext[1:] if ext else None

def convert_to_absolute_value_set(list_of_lists):
  """
  Converts a list of lists of integers (positive and negative) 
  to a set of their absolute values.

  Args:
    list_of_lists: A list of lists of integers.

  Returns:
    A set containing the absolute values of all integers 
    in the input lists.
  """
  absolute_values = set()
  for sublist in list_of_lists:
    for num in sublist:
      absolute_values.add(abs(num))
  return absolute_values

def double(literal):
    """
    Maps a literal value to its absolute double value.

    Args:
        literal: The literal to be mapped.
        
    Returns: 
        The duplicated mapped literal.
    """

    return 2 * abs(literal) + (1 if literal < 0 else 0)

def reduce_3sat_to_mock_1_in_3_3msat(clauses, max_variable):
    """
    Converts a 3SAT formula to a mock 1-IN-3-3SAT instance.

    Args:
        clauses: A list of 3CNF clauses.
        max_variable: The maximum variable in the input formula.

    Returns: A tuple (new_clauses, new_max_variable), where:
            - new_clauses: A list of mock 1-IN-3-3SAT clauses.
            - new_max_variable: The maximum variable in the new 3CNF formula.
    """

    new_clauses = []
    next_variable = 2 * max_variable + 2
    pivot = next_variable
    next_variable += 1

    variables = convert_to_absolute_value_set(clauses) # Set of all variables

    for variable in variables: # Keep consistency between x and ¬x
        positive_literal = double(variable) # Map variable to 2 * variable
        negative_literal = double(-variable)  # Map =variable to 2 * variable + 1

        new_clauses.extend([[positive_literal, negative_literal, pivot],
                            [positive_literal, negative_literal, -pivot],
                            [-positive_literal, -negative_literal, pivot],
                         [-positive_literal, -negative_literal, -pivot]])
    
    for clause in clauses: # Classic reduction from 3SAT to 1-IN-3-3SAT 
        # We map literals to positive variables
        x, y, z = double(clause[0]), double(clause[1]), double(clause[2])
        # monotone 3SAT clauses
        new_clauses.append([x, y, z])
    
    return new_clauses, next_variable - 1    

