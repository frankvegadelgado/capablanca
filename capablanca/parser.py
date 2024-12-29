import lzma
import bz2

from . import utils

def dimacs(lines):
    """Parses a DIMACS CNF file and returns a list of clauses.

    Args:
        lines: A list of lines from the DIMACS file.

    Returns:
        A list of clauses, where each clause is a list of literals.
    """

    clauses = []
    max_variable = 0

    for line in lines:
        line = line.strip()
        if not line.startswith('c') and not line.startswith('p'):
            clause = [int(literal) for literal in line.split(' ') if literal != '0']
            max_variable = max(max_variable, max(abs(literal) for literal in clause))
            clauses.append(clause)

    return clauses, max_variable

def read(filepath, ignore):
    """Reads a file and returns its lines in DIMACS format.

    Args:
        filepath: The path to the file.
        ignore: Ignore extension file

    Returns:
        A list of lines in DIMACS format.

    Raises:
        ValueError: If the file extension is not supported.
        FileNotFoundError: If the file is not found.
    """

    try:
        if ignore:
            with open(filepath, 'r') as file:
                lines = file.readlines()
        else:
            extension = utils.get_extension_without_dot(filepath)
            if extension == 'cnf':
                with open(filepath, 'r') as file:
                    lines = file.readlines()
            elif extension == 'xz' or extension == 'lzma':
                with lzma.open(filepath, 'rt') as file:
                    lines = file.readlines()
            elif extension == 'bz2' or extension == 'bzip2':
                with bz2.open(filepath, 'rt') as file:
                    lines = file.readlines()
            else:
                raise ValueError("Unsupported compressed file extension: " + str(extension))

        return dimacs(lines)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: " + str(filepath))
    except UnicodeDecodeError:
        raise ValueError("Invalid file format. Use the -u flag to decompress files before processing: " + str(filepath))