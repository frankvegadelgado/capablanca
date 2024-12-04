#                          SAT Solver
#                          Frank Vega
#                      December 3rd, 2024

import argparse
import sys
import time

from   satsolver           import *
from   z3solver            import *
from   reduction           import *
from   parser              import *
from   logging             import *
from   tester              import *

log = False
timed = False
started = 0.0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.')
    parser.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    
    args = parser.parse_args()

    log = args.verbose
    timed = args.timer
    
    console_output = ConsoleLogger(log)
    logger = SatLogger(console_output)
    
    # Read and parse a dimacs file
    
    logger.info("Pre-processing started")
    if timed:
        started = time.time()
    
    # Format from dimacs
    formula, initial_variable_map, max_variable = read(args.inputFile, 'cnf')
    
    if timed:
        logger.info(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Pre-processing done")
    
    logger.info("Starting the polynomial time reduction")
    if timed:
        started = time.time()
    
    # Polynomial Time Reduction
    clauses, tautology_set, variable_map, next_variable = reduce_to_3cnf(formula, initial_variable_map, max_variable)
    
    if timed:
        logger.info(f"Polynomial time reduction done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Polynomial time reduction done")
    
    logger.info("Starting the data structure creation")
    if timed:
        started = time.time()
    
    # Creating the data structure
    solver = build(clauses, variable_map)
    
    if timed:
        logger.info(f"Data structure creation done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Data structure creation")
    
    
    logger.info("Start solving the problem")
    if timed:
        started = time.time()
       
    # Solving in Exponential Time
    answer = solve_formula(solver, variable_map, tautology_set, initial_variable_map, max_variable)
    # Solving in Polynomial Time
    # answer = satsolver.solve_formula(...)
    
    if timed:
        logger.info(f"Solving the problem done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Solving the problem done")
    
    # Output the solution
    logger.info("Starting to check the solution")
    if timed:
        started = time.time()

    Satisfiability, solution = check(formula, answer, initial_variable_map)
    
    if timed:
        logger.info(f"Check the solution done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Check the solution done")

    if Satisfiability:
        print("s SATISFIABLE")
        sys.stdout.write("v ")
        for x in solution:
            sys.stdout.write("%s " % x)
        print("0")
    else:
        print("s UNSATISFIABLE")    