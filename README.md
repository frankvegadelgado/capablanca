# CAPABLANCA-SAT Solver
![](docs/capablanca.jpg)

# SAT Problem

Instance: A Boolean formula $\phi$ in CNF.

Question: Is $\phi$ satisfiable?
 
**Note: This problem is NP-complete (If any NP-complete can be solved in polynomial time, then $P = NP$)**.

# Theory

- A literal in a Boolean formula is an occurrence of a variable or its negation. A Boolean formula is in conjunctive normal form, or CNF, if it is expressed as an AND of clauses, each of which is the OR of one or more literals. 

- A truth assignment for a Boolean formula $\phi$ is a set of values for the variables in $\phi$. A satisfying truth assignment is a truth assignment that causes $\phi$ to be evaluated as true. A Boolean formula with a satisfying truth assignment is satisfiable. The problem SAT asks whether a given Boolean formula $\phi$ in CNF is satisfiable.

Example
----- 

Instance: The Boolean formula $(x_{1} \vee \rightharpoondown x_{3} \vee \rightharpoondown x_{2}) \wedge (x_{3} \vee x_{2} \vee x_{4})$ where $\vee$ (OR), $\wedge$ (AND) and $\rightharpoondown$ (NEGATION) are the logic operations.

Answer: Satisfiable (the formula is satisfiable when we assign simultaneously all the variables as true to obtain a satisfying truth assignment).

Input of this project
-----

The input is on [DIMACS](http://www.satcompetition.org/2009/format-benchmarks2009.html) formula with the extension .cnf.
  
The **file.cnf** on DIMACS format for $(x_{1} \vee \rightharpoondown x_{3} \vee \rightharpoondown x_{2}) \wedge (x_{3} \vee x_{2} \vee x_{4})$ is
```  
p cnf 4 2
1 -3 -2 0
3 2 4 0
```  

- The first line **p cnf 4 2** means there are 4 variables and 2 clauses.

- The second line **1 -3 -2 0** means the clause $(x_{1} \vee \rightharpoondown x_{3} \vee \rightharpoondown x_{2})$ (Note that, the number *0* means the end of the clause).

- The third line **3 2 4 0** means the clause $(x_{3} \vee x_{2} \vee x_{4})$ (Note that, the number *0* means the end of the clause).

# Compile and Environment

Downloading and Installing
-----

Install Python 3.10, 3.11, or 3.12.

Download and Install the NetworkX's Library version 3.3 and its dependencies 

If you use pip, you can install NetworkX's Library and its dependencies with:
-----
```
pip install networkx[default]
```
-----

# Build and Execute

To build and run from the command prompt:

```
git clone https://github.com/frankvegadelgado/capablanca.git
cd capablanca 
```

On capablanca directory run

```
python solver.py -i file.cnf
```

Finally, it would obtain in the console output:

```
s SATISFIABLE
```

# **SAT Benchmarks** 

We can run the DIMACS files with the extension .cnf in the simplest benchmarks folder:

```
>  python solver.py -i .\benchmarks\simplest\aim-50-1_6-yes1-1.cnf
s SATISFIABLE
```

and

```
> python solver.py -i .\benchmarks\simplest\aim-50-1_6-no-1.cnf
s UNSATISFIABLE
```

- We run each script and output the solutions for the satisfiable formulas.

We obtain this result since those files were copied into the directory capablanca\benchmarks\simplest:

```
aim-50-1_6-yes1-1.cnf
aim-50-1_6-no-1.cnf
```

from this well-known dataset [SAT Benchmarks](https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/DIMACS/AIM/descr.html). 

# Command Options

On capablanca directory if you run

```
python solver.py -h
```

then you will obtain the following output

```
usage: solver.py [-h] -i INPUTFILE [-v] [-t]

Solve an NP-complete problem from a DIMACS file.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        Input file path
  -v, --verbose         Enable verbose output
  -t, --timer           Enable timer output
```

where it is described all the possible options.

# Code

- Python code by **Frank Vega**.

# Complexity

````diff
+ We solve this problem in polynomial time.
+ Consequently, we deduce that P = NP.
````
 
# License
- MIT.