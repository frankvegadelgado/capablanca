# Created on 12/27/2024
# Author: Frank Vega

from . import app

def sat_solver_tests(total, logging=False, exponential_algorithm=False):

    # Run all sat solver test cases
    for i in range(total):
        print(f"Test: formula{i}.cnf")
        app.sat_solver(f'test_formulas/formula{i}.cnf', 
                         verbose=logging, 
                         timed=logging,
                         brute_force=exponential_algorithm)

# Run Tests
sat_solver_tests(total=4, logging=False, exponential_algorithm=True)