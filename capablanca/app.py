#                          SAT Solver
#                          CAPABLANCA
#                          Frank Vega
#                      January 19th, 2025

import argparse
import time
import networkx as nx
import z3
import pulp

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
    
    new_formula, line_graph, k = None, None, None
    # brute force

    if bruteForce:
        new_formula = formula
    else:
        line_graph, k = reduction.reduce_cnf_to_2xhs(formula, max_variable)
    
    if timed:
        utils.println(f"Polynomial-time reduction done in: {(time.time() - started) * 1000.0} milliseconds", logger)
    else:
        utils.println("Polynomial-time reduction done", logger)
    
    # Creating the Boolean Formula
    utils.println("Creating data structure started", logger)
    if timed:
        started = time.time()

    prob, solver = None, None     

    if bruteForce:
        solver = z3solver.build(new_formula)
    else:
        # Create a Linear Programming problem
        prob = pulp.LpProblem("MaximumIndependentSet", pulp.LpMaximize)

        # Create binary decision variables for each node in the line graph
        x = {node: pulp.LpVariable(f"x_{node}", cat="Binary") for node in line_graph.nodes}

        # Objective: Maximize the sum of selected nodes
        prob += pulp.lpSum(x[node] for node in line_graph.nodes), "MaximizeNumberOfSelectedEdges"

        # Constraints: For each edge in the line graph, ensure at most one endpoint is selected
        for u, v in line_graph.edges:
            prob += x[u] + x[v] <= 1, f"Conflict_{u}_{v}"

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
        # Solve the problem
        status = prob.solve()

        utils.println(f"{pulp.LpStatus[status]}", logger)

        # Extract the maximum independent set
        result = sum(pulp.value(x[node]) for node in line_graph.nodes)

        print(f"{result} >= {k}")
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
    helper.add_argument('--version', action='version', version='%(prog)s 1.5')
    
    # Initialize the parameters
    args = helper.parse_args()
    sat_solver(args.inputFile, 
               verbose=args.verbose, 
               timed=args.timer, 
               log=args.log,
               bruteForce=args.bruteForce)

if __name__ == "__main__":
    main()