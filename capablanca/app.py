#                          SAT Solver
#                          CAPABLANCA
#                          Frank Vega
#                      December 27th, 2024

import argparse
import time

from . import reduction
from . import parser
from . import applogger
from . import z3solver

logger = None

def println(msg):
    global logger
    logger.info(msg)

def output(msg, use_logs):
    if use_logs:
        println(msg)
    else:
        print(msg)
    
def sat_solver(inputFile, verbose=False, timed=False, log=False, unzip=False, brute_force=False):
    """Solves a CNF formula.

    Args:
        inputFile: Input file path.
        verbose: Enable verbose output.
        timed: Enable timer output.
        log: Enable file logging.
        unzip: Unzip file input.
        brute_force: True (Exponential Solution), False (Feasible Solution)
    """
    
    global logger

    logger = applogger.Logger(applogger.FileLogger() if (log) else applogger.ConsoleLogger(verbose))
    started = 0.0
    
    # Read and parse a dimacs file
    println("Pre-processing started")
    if timed:
        started = time.time()
    
    formula, max_variable = parser.read(inputFile, not unzip)
    
    if timed:
        started = (time.time() - started) * 1000.0
        println("Pre-processing done in: " + str(started) + " milliseconds")
    else:
        println("Pre-processing done")
    
    # Polynomial Time Reduction
    println("Reducing the problem started")
    if timed:
        started = time.time()
    
    new_clauses = reduction.reduce_cnf_to_3sat(formula, max_variable) if (brute_force) else reduction.reduce_cnf_to_xor_sat(formula, max_variable)
    
    if timed:
        started = (time.time() - started) * 1000.0
        println("Reducing the problem done in: " + str(started) + " milliseconds")
    else:
        println("Reducing the problem done")

    # Creating the Boolean Formula
    println("Creating data structure started")
    if timed:
        started = time.time()
        
    solver = z3solver.build_brute_force(new_clauses) if (brute_force) else z3solver.build(new_clauses)
    
    if timed:
        started = (time.time() - started) * 1000.0
        println("Creating data structure done in: " + str(started) + " milliseconds")
    else:
        println("Creating data structure done")
  
    # Solving the Boolean Formula in Polynomial Time
    println("Solving the problem started")
    if timed:
        started = time.time()
        
    satisfiability, answer = z3solver.solve_brute_force(solver, formula, max_variable) if (brute_force) else z3solver.solve(solver, formula, max_variable)
    
    if timed:
        started = (time.time() - started) * 1000.0
        println("Solving the problem done in: " + str(started) + " milliseconds")
    else:
        println("Solving the problem done")
  
    # Output the solution
    answer = "s UNKNOWN" if (satisfiability is None) else ("s SATISFIABLE" + '\n' + "v " + ' '.join(map(str, answer)) + " 0" if (satisfiability) else "s UNSATISFIABLE")
    output(answer, verbose or log)    
        
def main():
    
    
    # Define the parameters
    helper = argparse.ArgumentParser(prog="jaque", description='Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.')
    helper.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    helper.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    helper.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    helper.add_argument('-l', '--log', action='store_true', help='Enable file logging')
    helper.add_argument('-u', '--unzip', action='store_true', help='Unzip file input')
    
    # Initialize the parameters
    args = helper.parse_args()
    sat_solver(args.inputFile, 
               verbose=args.verbose, 
               timed=args.timer, 
               log=args.log,
               unzip=args.unzip,
               brute_force=True)

if __name__ == "__main__":
    main()