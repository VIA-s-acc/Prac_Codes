# PracCodes

## Table Of Content
### Gauss
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Gauss">Gauss|Chol(V1,V2) Code</a></em></p>
<ul>
    <li><a href="#Gauss-|-Chol">Gauss | Chol Methods</a></li>
    <li><a href="#LinEqSolver">LinEqSolver</a></li>
    <li><a href="#Methods">Methods</a></li>
    <li><a href="#Usage">Usage</a></li>
</ul>



## Gauss | Chol

Gauss | Chol(v1,v2) Methods

### LinEqSolver

The LinEqSolver class provides methods for solving systems of linear equations and working with matrices and vectors.

### Methods:

-    `det(matrix)`: Calculates the determinant of a square matrix.
-    `gauss_elimination(matrix, vec, dig)`: Performs Gaussian elimination to solve a system of linear equations.
-    `generate_random_matrix(size, rng, mode)`: Generates a random matrix of the given size.
-    `save_matrix_to_file(matrix, filename)`: Saves the given matrix to a file.
-    `read_matrix_from_file(filename)`: Reads a matrix from a file.
-    `generate_random_vector(size, rng):` Generates a random vector of the specified size and range.
-    `save_vector_to_file(vector, filename)`: Saves the given vector to a file.
-    `read_vector_from_file(filename)`: Reads a vector from a file.
-    `_check_solve_web(matrix, b, size, dig, solution, epsilon)`: Solves a system of linear equations using a web-based matrix calculator and checks the solution.
-    `LU_decomposition(matrix)`: Performs LU decomposition on the given matrix.
-    `_signum(num)`: Calculates the signum of the given number.
-    `cholesky_decomposition_v2(matrix)`: Performs Cholesky decomposition on the given matrix.
-    `_sylvesters_criterion(matrix)`: Checks if the given matrix satisfies Sylvester's criterion for positive definiteness.
-    `cholesky_decomposition_v1(matrix)`: Performs Cholesky decomposition on the given matrix.
-    `_matrix_multiply(*matrices)`: Performs matrix multiplication on the input matrices.
-    `_chol_solver(matrix, vec, dig, mode)`: Solves a linear system using Cholesky decomposition or LU decomposition.
-    `_lu_solver(matrix, vec, dig)`: Solves a linear system of equations using LU decomposition.
-    `_forward_substitution(matrix, vec, dig)`: Solves a system of linear equations using forward substitution.
-    `_backward_substitution(matrix, vec, dig)`: Solves a system of linear equations using backward substitution.
-    `generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig, check, epsilon, m_v_range, mode, random, **kwargs)`: Generates and solves a system of linear equations, with options for different solving methods and file saving options.

### Usage:

```python
from LinEq import LinEqSolver

# Example usage
matrix = [[2, 1], [1, -1]]
vector = [8, -1]

# Calculate determinant
determinant = LinEqSolver.det(matrix)

# Solve system of linear equations
solution = LinEqSolver.gauss_elimination(matrix, vector)

# Generate random matrix and vector
random_matrix = LinEqSolver.generate_random_matrix(2)
random_vector = LinEqSolver.generate_random_vector(2)

# Save matrix and vector to files
LinEqSolver.save_matrix_to_file(random_matrix, "random_matrix.txt")
LinEqSolver.save_vector_to_file(random_vector, "random_vector.txt")

# Read matrix and vector from files
read_matrix = LinEqSolver.read_matrix_from_file("random_matrix.txt")
read_vector = LinEqSolver.read_vector_from_file("random_vector.txt")
```

or 
```python

from LinEq import *

matrix =   [[2,-1,0],
            [-1,2,-1],
            [0,-1,2]] 
vec = [-8, -3, 6]

LinEqSolver.generate_and_solve_linear_equations(3, 'Gauss/eq/matrix.txt', 'Gauss/eq/vec.txt', 'Gauss/eq/sol.txt', 'Gauss/eq/sol_ext.txt',dig = 5, m_v_range=(10,10),check=False, mode = 'chol_v1', random = False, matrix = matrix, vector = vec)  

```


or 
```python
from LinEq import *

LinEqSolver.generate_and_solve_linear_equations(3, 'Gauss/eq/matrix.txt', 'Gauss/eq/vec.txt', 'Gauss/eq/sol.txt', 'Gauss/eq/sol_ext.txt',dig = 5, m_v_range=(10,10),check=False, mode = 'chol_v1', random = True)  

```
