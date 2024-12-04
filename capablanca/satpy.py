#                          SAT Solver
#                          Frank Vega
#                      December 4th, 2024

import argparse
import sys
import time

from . import satsolver
from . import z3solver
from . import reduction
from . import parser
from . import satlogger
from . import tester

log = False
timed = False
started = 0.0

if __name__ == "__main__":

    helper = argparse.ArgumentParser(description='Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.')
    helper.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    helper.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    helper.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    
    args = helper.parse_args()

    log = args.verbose
    timed = args.timer
    
    logger = satlogger.SatLogger(satlogger.ConsoleLogger(log))
    
    # Read and parse a dimacs file
    
    logger.info("Pre-processing started")
    if timed:
        started = time.time()
    
    # Format from dimacs
    formula, initial_variable_map, max_variable = parser.read(args.inputFile, 'cnf')
    
    if timed:
        logger.info(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Pre-processing done")
    
    logger.info("Starting the polynomial time reduction")
    if timed:
        started = time.time()
    
    # Polynomial Time Reduction
    clauses, tautology_set, variable_map, next_variable = reduction.reduce_to_3cnf(formula, initial_variable_map, max_variable)
    
    if timed:
        logger.info(f"Polynomial time reduction done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Polynomial time reduction done")
    
    logger.info("Starting the data structure creation")
    if timed:
        started = time.time()
    
    # Creating the data structure
    solver = z3solver.build(clauses, variable_map)
    
    if timed:
        logger.info(f"Data structure creation done in: {(time.time() - started) * 1000.0} milliseconds")
    else:
        logger.info("Data structure creation")
    
    
    logger.info("Start solving the problem")
    if timed:
        started = time.time()
       
    # Solving in Exponential Time
    answer = z3solver.solve_formula(solver, variable_map, tautology_set, initial_variable_map, max_variable)
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

    Satisfiability, solution = tester.check(formula, answer, initial_variable_map)
    
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