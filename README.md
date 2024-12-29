# CAPABLANCA-SAT Solver

![Jose Raul Capablanca (Third World Chess Champion from 1921 to 1927)](docs/capablanca.jpg)

# Boolean Satisfiability (SAT) Problem

**Problem:** Given a Boolean formula in Conjunctive Normal Form (CNF), is there a truth assignment that makes the formula evaluate to true?

**Background:**

The Boolean Satisfiability Problem (SAT) is a fundamental problem in computer science. It is known to be NP-complete, which means that any problem whose solution can be verified in polynomial time can be reduced to SAT. This implies that SAT is likely to be computationally difficult, although there is no proof of this.

**Concepts:**

- **Literal:** A variable or its negation (e.g., $x$ or $\neg x$).
- **Clause:** A disjunction (OR) of one or more literals (e.g., $x \vee \neg y \vee z$).
- **Conjunctive Normal Form (CNF):** A Boolean formula where each clause is connected by conjunction (AND).
- **Truth Assignment:** An assignment of truth values (true or false) to all variables in a formula.
- **Satisfying Truth Assignment:** A truth assignment that makes a formula evaluate to true.
- **Satisfiable Formula:** A formula that has a satisfying truth assignment.

**Example:**

Consider the formula $(x_1 \vee ¬x_3 \vee ¬x_2) \wedge (x_3 \vee x_2 \vee x_4)$, where $\vee$ (OR), $\wedge$ (AND) and $\neg$ (NEGATION) are the logic operations. This formula is in CNF with four variables ($x_1$, $x_2$, $x_3$, and $x_4$) and two clauses. A possible satisfying truth assignment is {$x_1$: True, $x_2$: True, $x_3$: True, $x_4$: True}.

**Input format:**

The input for SAT solvers is typically provided in [DIMACS](https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html) format (`.cnf` files). A DIMACS file consists of three parts:

1. **Header:** The first line specifies the number of variables (n) and clauses (m) in the formula using the format `p cnf n m`.
2. **Clauses:** Each subsequent line represents a clause, where each literal is represented by a variable's index (positive for the variable, negative for its negation). A zero at the end of the line indicates the end of the clause.

**Example `.cnf` file:**

```
p cnf 4 2
1 -3 -2 0
3 2 4 0
```

This is a `.cnf` file representing a Boolean formula in Conjunctive Normal Form (CNF) for the Boolean Satisfiability Problem (SAT). Let's break down what each line means:

- **Header (p cnf 4 2):**

  - `p cnf` indicates it's a CNF formula in DIMACS format.
  - `4` specifies the number of variables in the formula ($x_1$, $x_2$, $x_3$, and $x_4$ in this case).
  - `2` specifies the number of clauses (disjunctions of literals) in the formula.

- **Clauses (1 -3 -2 0 and 3 2 4 0):**
  - Each line represents a clause.
  - A positive integer represents a variable (e.g., `1` represents variable $x_1$).
  - A negative integer represents the negation of a variable (e.g., `-3` represents $\neg x_3$).
  - `0` at the end of the line indicates the end of the clause.

**Explanation of the clauses:**

- `1 -3 -2 0`: This clause translates to $(x_1 \vee \neg x_3 \vee \neg x_2)$, which means at least one of $x_1$, $\neg x_3$, or $\neg x_2$ must be true for the clause to be true.
- `3 2 4 0`: This clause translates to $(x_3 \vee x_2 \vee x_4)$, which means at least one of $x_3$, $x_2$, or $x_3$ must be true for the clause to be true.

**In essence, the formula represented by this `.cnf` file is asking if there exists an assignment of truth values (true or false) to the variables $x_1$, $x_2$, $x_3$, and $x_4$ that makes both clauses true simultaneously.**

## Installation and Setup

**1. Install Python:**

- Ensure you have Python 3.8 or a later version installed on your system. You can download and install it from the official Python website: https://www.python.org/downloads/

**2. Install Capablanca's Library:**

- Open your terminal or command prompt.
- Use `pip` to install the Capablanca library and its dependencies:

```
pip install capablanca
```

## Running the SAT Solver with Capablanca

**Using Capablanca's built-in benchmarks:**

1. **Install Capablanca's library:**

   If you haven't already, follow the installation steps in the previous section to install Capablanca.

2. **Download Capablanca's library:**

   Download the benchmarks from the GitHub repository.

   ```
   git clone https://github.com/frankvegadelgado/capablanca.git
   ```

3. **Execute the script:**

   Open your terminal or command prompt and navigate to the directory where you downloaded Capablanca (e.g., using `cd capablanca`).

   Run the following command to solve a sample `.cnf` file named `file.cnf` included with Capablanca's benchmarks:

   ```
   jaque -i benchmarks/simple/file.cnf
   ```

Capablanca supports compressed `.cnf` files, including `.xz`, `.lzma`, `.bz2`, and `.bzip2` formats.

**Output Interpretation:**

## If the formula is satisfiable, the console output will display:

```
s SATISFIABLE
v 1 2 3 4 0
```

- **`s SATISFIABLE`:** This line indicates that the SAT solver found a satisfying truth assignment for the given formula.
- **`v 1 2 3 4 0`:** This line provides the satisfying truth assignment.
  - Positive numbers (e.g., `1`, `2`, `3`, `4`) represent variables assigned the value "True."
  - `0` marks the end of the truth assignment.

## If the formula is unsatisfiable, the console output will display:

```
s UNSATISFIABLE
```

## SAT Benchmarks and Testing

Capablanca includes a collection of sample `.cnf` files in the `benchmarks/file-dimacs-aim` directory. These files can be used to test the functionality of the SAT solver. The files are derived from the well-known [SAT Benchmarks](https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/DIMACS/AIM/descr.html) dataset.

**Running Sample Benchmarks:**

1. **Ensure Capablanca is installed:** Follow the installation steps in the previous section if you haven't already installed Capablanca.

2. **Execute the script:** Open your terminal or command prompt and navigate to the directory where Capablanca was downloaded.

You can then use the `jaque` command to run the sample benchmarks. For example, the following commands demonstrate running two sample files:

- Test the satisfiable formula `aim-50-1_6-yes1-1.cnf`:

  ```
  jaque -i benchmarks/file-dimacs-aim/aim-50-1_6-yes1-1.cnf
  s SATISFIABLE
  v 2 3 7 8 9 14 17 18 19 20 21 22 23 24 26 27 28 30 31 35 36 38 39 40 41 42 43 46 48 -50 -49 -47 -45 -44 -37 -34 -33 -32 -29 -25 -16 -15 -13 -12 -11 -10 -6 -5 -4 -1 0
  ```

A satisfiable formula means there exists a truth assignment that makes the formula true. The output will indicate this with s SATISFIABLE followed by the satisfying truth assignment.

- Test the unsatisfiable formula `aim-50-1_6-no-1.cnf`:

  ```
  jaque -i benchmarks/file-dimacs-aim/aim-50-1_6-no-1.cnf
  s UNSATISFIABLE
  ```

running these sample benchmarks, you can verify that Capablanca is functioning correctly and gain experience using the `jaque`

## Command-Line Options

To view the available command-line options for the `jaque` command, use the following command in your terminal or command prompt:

```
jaque -h
```

This will display the help message, which provides information about the available options and their usage:

```
usage: jaque [-h] -i INPUTFILE [-v] [-t] [-l] [-u]

Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        Input file path
  -v, --verbose         Enable verbose output
  -t, --timer           Enable timer output
  -l, --log             Enable file logging
  -u, --unzip           Unzip file input
```

Available Options:

    -h, --help: Displays this help message and exits the program.
    -i INPUTFILE, --inputFile INPUTFILE: Specifies the path to the input file containing the Boolean formula. This option is required.
    -v, --verbose: Enables verbose output, providing more detailed information about the solver's progress.
    -t, --timer: Enables timer output, displaying the time taken by the solver to find a solution.
    -l, --log: Enables file logging, writing detailed information about the solver's execution to a log file.
    -u, --unzip: Unzip compressed input files before processing.

By using these command-line options, you can customize the behavior of the `jaque` command to suit your specific needs.

## Implementation

- **Programming Language:** Python
- **Author:** Frank Vega

## Complexity

```diff
- The current implementation of the SAT solver likely uses a brute-force approach, which can be computationally expensive for larger and more complex problems.
```

## License

This code is released under the MIT License.
