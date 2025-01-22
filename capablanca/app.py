#                          SAT Solver
#                          CAPABLANCA
#                          Frank Vega
#                      January 19th, 2025

import argparse
import time
import networkx as nx
import z3

from . import reduction
from . import parser
from . import applogger
from . import utils
from . import z3solver

def sat_solver(inputFile, verbose=False, timed=False, log=False, bruteForce=False):
    """Solves a CNF formula.

    Args:
        inputFile: Input file path.
        verbose: Enable verbose output.
        timed: Enable timer output.
        log: Enable file logging.
        unzip: Unzip file input.
    """
    
    logger = applogger.Logger(applogger.FileLogger() if (log) else applogger.ConsoleLogger(verbose))
    started = 0.0
    
    # Read and parse a dimacs file
    utils.println("Pre-processing started", logger)
    if timed:
        started = time.time()
    
    formula, max_variable = parser.read(inputFile)
    
    if timed:
        utils.println(f"Pre-processing done in: {(time.time() - started) * 1000.0} milliseconds", logger)
    else:
        utils.println("Pre-processing done", logger)
    
    # Polynomial-time reduction
    utils.println("Polynomial-time reduction started", logger)
    if timed:
        started = time.time()
    
    new_formula, sets, k = None, None, None
    # brute force

    if bruteForce:
        new_formula = formula
    else:
        sets, k = reduction.reduce_cnf_to_3xsp(formula, max_variable)
    
    if timed:
        utils.println(f"Polynomial-time reduction done in: {(time.time() - started) * 1000.0} milliseconds", logger)
    else:
        utils.println("Polynomial-time reduction done", logger)
    
    # Creating the Boolean Formula
    utils.println("Creating data structure started", logger)
    if timed:
        started = time.time()

    G, solver = None, None     

    if bruteForce:
        solver = z3solver.build(new_formula)
    else:
        G = nx.Graph()
        for key1, subset1 in enumerate(sets):
            for key2, subset2 in enumerate(sets):
                if key1 < key2 and subset1.intersection(subset2):
                    G.add_edge(key1, key2)
            
        
    if timed:
        utils.println(f"Creating data structure done in: {(time.time() - started) * 1000.0} milliseconds", logger)
    else:
        utils.println("Creating data structure done", logger)
  
    # Solving the Boolean Formula in Polynomial Time
    utils.println("Solving the problem started", logger)
    if timed:
        started = time.time()

    satisfiability = None

    if bruteForce:
        answer = solver.check()
        if answer == z3.unsat:
            satisfiability = False
        elif answer == z3.sat:
            satisfiability = True

    else:
        result = None   
        try:
            result = len(nx.algorithms.matching.max_weight_matching(G, maxcardinality=True))   
        except Exception as e:
            result = 0 
        
        satisfiability = result >= k
        
    if timed:
        utils.println(f"Solving the problem done in: {(time.time() - started) * 1000.0} milliseconds", logger)
    else:
        utils.println("Solving the problem done", logger)
  
    # Output the solution
    answer = "s UNKNOWN" if (satisfiability is None) else ("s SATISFIABLE" if (satisfiability) else "s UNSATISFIABLE")
    utils.output(answer, logger, verbose or log)    
        
def main():
    
    
    # Define the parameters
    helper = argparse.ArgumentParser(prog="jaque", description='Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.')
    helper.add_argument('-i', '--inputFile', type=str, help='Input file path', required=True)
    helper.add_argument('-b', '--bruteForce', action='store_true', help='using a brute-force approach')
    helper.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    helper.add_argument('-t', '--timer', action='store_true', help='Enable timer output')
    helper.add_argument('-l', '--log', action='store_true', help='Enable file logging')
    helper.add_argument('--version', action='version', version='%(prog)s 1.3')
    
    # Initialize the parameters
    args = helper.parse_args()
    sat_solver(args.inputFile, 
               verbose=args.verbose, 
               timed=args.timer, 
               log=args.log,
               bruteForce=args.bruteForce)

if __name__ == "__main__":
    main()