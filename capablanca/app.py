#                   Minimum Vertex Cover Solver
#                          Frank Vega
#                      Juanary 30th, 2025

import argparse
import time

from . import algorithm
from . import parser
from . import applogger
from . import utils


def main():
    
    # Define the parameters
    helper = argparse.ArgumentParser(prog="cover", description='Estimating the Minimum Vertex Cover with an approximation factor smaller than √2 for an undirected graph encoded as a Boolean adjacency matrix stored in a file.')
    helper.add_argument('-i', '--inputFile', type=str, help='input file path', required=True)
    helper.add_argument('-a', '--approximation', action='store_true', help='enable comparison with a polynomial-time approximation approach within a factor of 2')
    helper.add_argument('-b', '--bruteForce', action='store_true', help='enable comparison with the exponential-time brute-force approach')
    helper.add_argument('-c', '--count', action='store_true', help='calculate the size of the vertex cover')
    helper.add_argument('-v', '--verbose', action='store_true', help='anable verbose output')
    helper.add_argument('-l', '--log', action='store_true', help='enable file logging')
    helper.add_argument('--version', action='version', version='%(prog)s 2.1')
    
    # Initialize the parameters
    args = helper.parse_args()
    filepath = args.inputFile
    logger = applogger.Logger(applogger.FileLogger() if (args.log) else applogger.ConsoleLogger(args.verbose))
    count = args.count
    brute_force = args.bruteForce
    approximation = args.approximation
    # Read and parse a dimacs file
    logger.info(f"Parsing the Input File started")
    started = time.time()
    
    sparse_matrix = parser.read(filepath)
    filename = utils.get_file_name(filepath)
    logger.info(f"Parsing the Input File done in: {(time.time() - started) * 1000.0} milliseconds")
    
    logger.info("An Approximate Solution with an approximation ratio of less than √2 started")
    started = time.time()
    
    result = algorithm.find_vertex_cover(sparse_matrix)

    logger.info(f"An Approximate Solution with an approximation ratio of less than √2 done in: {(time.time() - started) * 1000.0} milliseconds")

    answer = utils.string_result_format(result, count)
    output = f"{filename}: {answer}"
    utils.println(output, logger, args.log)
    
    if approximation:
        logger.info("An Approximate Solution with an approximation ratio of 2 started")
        started = time.time()
        
        result = algorithm.find_vertex_cover_approximation(sparse_matrix)

        logger.info(f"An Approximate Solution with an approximation ratio of 2 done in: {(time.time() - started) * 1000.0} milliseconds")
        
        answer = utils.string_result_format(result, count)
        output = f"{filename}: (Approximation) {answer}"
        utils.println(output, logger, args.log)

    if brute_force:
        logger.info("A solution with an exponential-time complexity started")
        started = time.time()
        
        result = algorithm.find_vertex_cover_brute_force(sparse_matrix)

        logger.info(f"A solution with an exponential-time complexity done in: {(time.time() - started) * 1000.0} milliseconds")
        
        answer = utils.string_result_format(result, count)
        output = f"{filename}: (Brute Force) {answer}"
        utils.println(output, logger, args.log)
    
if __name__ == "__main__":
    main()