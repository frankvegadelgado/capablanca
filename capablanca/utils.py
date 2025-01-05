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