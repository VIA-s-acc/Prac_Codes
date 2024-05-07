# PracCodes

## Table Of Content

<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq">Lineq Source</a></em></p>

- [Linear Equations Classes](#lineq-classes)
    -   [Checker](#checker)
    -   [Generator](#generator)
    -   [Matrix Methods](#matrix-methods)
    -   [Save And Read](#save-and-read)
        -   [Saver](#saver)
        -   [Reader](#reader)
    -   [LinEqSolver](#lineqsolver)

- [Non-Linear Equations Classes](#non-linear-equations-classes)
    -   [Polynomial](#polynomial)
    -   [NonLinEqSolver](#nonlineqsolver)
    -   [Prettier Poly](#prettier-poly)
    -   [Interpolation](#interpolation)

- [Numerical Integration](#numerical-integration)
    -   [Integration](#integration)

- [Math Physics equations (Numeric)](#math-physics-equations-numeric)
    - [MPE](#mpe)
    - [Plotter](#plotter)


## Lineq Classes 
This classes is a linear equation solver system that provides methods for performing various operations related to solving systems of linear equations. Here's a brief summary of each class method:
### Checker
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Checkers.py">Checker Source</a></em></p>
This `Checker` class contains three methods:

1. `_signum(num)`: 
    - Calculates the signum of the given number.

2. `_check_solve_web(matrix, b, size, dig, solution, epsilon)`: 
    - Solves a system of linear equations using a web-based matrix calculator.

3. `_sylvesters_criterion(matrix)`: 
    - Checks if the given matrix satisfies Sylvester's criterion for positive definiteness.

4. `_diagonal_domination(matrix)`:
    - Checks if the given matrix is diagonal dominant.

5.  `_symmetric_check(matrix)`:
    - Checks if the given matrix is symmetric.

### Generator
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Generator.py">Generator Source</a></em></p>

This class Generator contains two static methods:

1.  `generate_random_matrix(size, rng: int = 10, mode: str = None)`:
    - Generates a random matrix of the given size, with an optional mode for symmetric or 3-diagonal matrix.

2.  `generate_random_vector(size, rng: int = 10)`:
    - Generates a random vector of the specified size and range.

### Matrix Methods 
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Matrix_methods.py">Matrix Methods Source</a></em></p>

This class contains methods for various matrix operations:

1.  `det(matrix)`: 
    - Calculates the determinant of a square matrix.

2. `LU_decomposition(matrix)`: 
    - Performs LU decomposition on the given matrix and returns the lower and upper triangular matrices.

3. `cholesky_decomposition_v1(matrix)`: 
    - Performs Cholesky decomposition and returns the lower and upper triangular matrices.

4. `cholesky_decomposition_v2(matrix)`: 
    - Performs Cholesky decomposition and returns the lower triangular matrix, diagonal matrix, and upper triangular matrix.

5. `_matrix_multiply(*matrices)`:
    - Performs matrix multiplication on the input matrices and returns the resulting matrix.

6. `euclidean_norm(vec)`: 
    - Calculates the Euclidean norm of a vector.

7. `_scalar_matrix_multiply(scalar, matrix)`: 
    - Performs matrix multiplication on the input matrices and returns the resulting matrix.    

8. `_vector_matrix_multiply(matrix, vector)`: 
    - Multiply a matrix by a vector and return the resulting vector.

9. `_vector_approximation(v1, v2, tol=1e-6)`: 
    - Check if two vectors are approximately equal within a tolerance.

10. `_inverse_matrix(matrix)`: 
    - Calculate the inverse of a matrix using Gauss-Jordan elimination.

11. `eigen_get(matrix, max_iter=100, eps=1e-6)`: 
    - Calculate the max_min eigenvalues and eigenvectors of the given matrix using the power method algorithm.

12. `power_method(matrix, max_iter=100, eps=1e-6)`: 
    - Perform the power method to find the dominant eigenvalue and eigenvector of the given matrix.


### Save And Read
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/S_R.py">Save And Read Source</a></em></p>

#### Reader
This `Reader` class has two methods:

1.  `read_matrix_from_file(filename)`: 
    - Reads a matrix from a file and returns a 2D list representing the matrix.
    
2.  `read_vector_from_file(filename)`: 
    - Reads a vector from a file and returns a list containing the integers read from the file.

#### Saver
This class, `Saver`, provides methods to save matrices and vectors to files, and to combine text files into a single output file.

1.  `save_matrix_to_file`: 
    - Saves the given matrix to a file, with an optional 'prettier' mode for formatting.

2.  `save_vector_to_file`: 
    - Saves the given vector to the specified file.

3.  `_combine_txt`: 
    - Combines text files in a specified folder into a single output file, with an option to delete the input text files after combining.

### Prettier
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Prettier.py">Prettier Source</a></em></p>

This class, `Prettier`, contains a method `_pretty_matrix` that generates a pretty matrix representation with column labels, row numbers, and proper spacing. 

1.  `_pretty_matrix(matrix)`: 
    - Generates a pretty matrix representation with column labels, row numbers, and proper spacing.


### LinEqSolver
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/lineq.py">LinEqSolver Source</a></em></p>

This class is a linear equation solver that provides methods for performing various operations related to solving systems of linear equations. Here's a brief summary of each class method:

1.  `gauss_elimination(matrix, vec, dig)`: 
    - Performs Gaussian elimination to solve a system of linear equations.

2.  `tridiagonal_elimination(matrix, vec, dig)`: 
    - Performs Tridiagonal elimination to solve a system of linear equations.

3.  `_select_omega(matrix, eigen_max_iter, eigen_eps)`: 
    - Selects the relaxation parameter for the relaxation method.

4.  `simple_iteration(matrix, vec, max_iter, eigen_max_iter, eigen_eps, eps, dig)`: 
    - Performs simple iteration to solve a system of linear equations.

5.  `seidel_iteration(matrix, vec, dig)`: 
    - Performs Seidel iteration to solve a system of linear equations.

6.  `jacobi_iteration(matrix, vec, max_iter, eps, dig)`: 
    - Performs Jacobi iteration to solve a system of linear equations.

7.  `relaxation_method(matrix, vec, dig, omega)`: 
    - Performs relaxation method to solve a system of linear equations.

8.  `explicit_iteration(matrix, vec, dig)`: 
    - Performs explicit iteration to solve a system of linear equations.
    
9.  `min_res_iteration(matrix, vec, max_iter, eps, dig)`: 
    - Performs minimum residual iteration to solve a system of linear equations.

10. `min_chg_iteration(matrix, vec, max_iter, eps, dig, matrix_choose_mode)`: 
    - Performs minimum change iteration to solve a system of linear equations.

11. `step_desc_iteration(matrix, vec, max_iter, eps, dig)`: 
    - Performs method of steepest descent to solve a system of linear equations.
    
12. `step_desc_iteration_imp(matrix, vec, max_iter, eps, dig, matrix_choose_mode)`: 
    - Performs implicit method of steepest descent to solve a system of linear equations.

13. `_chol_solver(matrix, vec, dig, mode)`:
    - Solves a linear system using Cholesky decomposition.

14. `_lu_solver(matrix, vec, dig):` 
    - Solves a linear system of equations using LU decomposition.

15. `_forward_substitution(matrix, vec, dig)`: 
    - Solves a system of linear equations using forward substitution.

16. `_backward_substitution(matrix, vec, dig)`: 
    - Solves a system of linear equations using backward substitution.

17. `generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig, check, epsilon, m_v_range, mode, random, prettier_path, prettier, logger, **kwargs)`: 
    - Generates and solves a system of linear equations, with various options for customization and output.


## Non-Linear Equations Classes


### Polynomial
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Nonlineq/NonLinEq/Utils/Poly.py">Poly Source</a></em></p>
A class for representing polynomials

1.  `__init__(self, Poly)`: 
    - Initialize the polynomials

2.  `__str__(self)`: 
    - Return a string representation of the Degree and Polynomial attributes with special character replacements.

3.  `__eq__(self, other)`: 
    - Check if two polynomials are equal.

4.  `__neq__(self, other)`: 
    - Check if two polynomials are not equal.

5.  `__add__(self, other)`: 
    - Add two polynomials.

6.  `__sub__(self, other)`: 
    - Subtract two polynomials.

7.  `__mul__(self, other)`: 
    - Multiply two polynomials.

8.  `__rmul__(self, other)`: 
    - Multiply a polynomial by a constant.

9.  `__neg__(self)`: 
    - Negate the polynomial.

10. `__call__(self, value)`: 
    - Evaluate the polynomial expression with the given value for the variable.

11. `polynomial_degree(poly_str)`: 
    - A method to calculate the degree of a polynomial expression.

12. `eval(self, value)`: 
    - Evaluate the polynomial expression with the given value for the variable.

13. `get_degree(self)`: 
    - A method to retrieve the degree attribute from the object.

14. `get_variable(self)`: 
    - Get the value of the Variable attribute.

15. `get_coeffs(self)`: 
    - Get the coefficients of the polynomial.

16. `copy(self)`: 
    - Create a copy of the polynomial.

17. `get_diff(self)`: 
    - Get the derivative of the polynomial.   

18. `plot(self, range, step, colors, legend, **kwargs)`: 
    - Plot the polynomial.

### NonLinEqSolver
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Nonlineq/NonLinEq/Nonlineq.py">NonLinEq Source</a></em></p>
A class for solving non-linear equations

1.  `solve(self, eps, mode, step)`: 
    - Solve the non-linear equation

2.  `bisect_solver(self, eps, step)`: 
    - Use Bisection method for solving the equation P(n) = 0

3.  `find_intervals_with_opposite_signs(self, start, end, step)`: 
    - Find the intervals with opposite signs in the domain

4.  `newton_solver(self, eps, step)`: 
    - Use Newton method for solving the equation P(n) = 0

5.  `iter_sim_solver(self, eps, step, max_iter)`: 
    - Use simple Iterative method for solving the equation P(n) = 0

### Prettier Poly
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Nonlineq/NonLinEq/Utils/Prettier.py">Prettier Source</a></em></p>
Class for pretty printing polynomials.
    
1. `pretty_polynom(Poly)`: 
    - Pretty string representation of the polynomial

### Interpolation
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Nonlineq/NonLinEq/Utils/Inter.py">Interpolation Source</a></em></p>
Class that Interpolates a function using the specified interpolation mode and points.

1.  `generate_vandermonde(x)`: 
    - generates the Vandermonde matrix
2.  `interpolate(func, mode, points, intervals=(0, 1, 10), **kwargs)`: 
    - interpolates the function

3.  `lagrange_interpolation(x, y, var)`: 
    - lagrange interpolation

4.  `newton_interpolation(x, y, var)`: 
    - newton interpolation

5.  `divided_diff(x, y)`: 
    - calculates the divided difference table

6.  `cspline_interpolation(x, y, x_y_intervals, var)`: 
    - cubic spline interpolation
    

## Numerical Integration

### Integration
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Numintegrate/NumIntegrate/Integration.py">Integration Source</a></em></p>

Class for numerical integration

1. `squares(mode)`: 
    - Calculate the integral using the sum of squares

2. `Simpson()`: 
    - Calculate the integral using Simpson method

3.  `Trapeze()`:
    - Calculate the  integrals using trapeze method

## Math Physics Equations Numeric

### MPE
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/MathPhysEqs/MPE/mpe.py">MPE Source</a></em></p>
Class for solving MPE 

dy/dx = f(x, y) 

y(x0) = y0

f must be function of x,y
Example:
-------
def f(x,y):
    return -x+y

1. `init(self, Area, f, f0)`:
    - initialization of MPE solver

2.  `eiler(self, n)`: 
    - Eiler method

3.  `heun(self, n)`: 
    - Heun method

4.  `-k_step_Adams_explicit(self, k)`: 
    - K step Adams explicit method

5.  `rk4(self, n)`: 
    - Runge-Kutta 4 order method

6.  `rk2(self, n)`: 
    - Runge-Kutta 2 order method

7.  `solve_Adams_KSE(self, k, n, preliminary_k_method)`: 
    - Solve using K step Adams explicit method
    
### Plotter
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/MathPhysEqs/MPE/Utils/plotter.py">Plotter Source</a></em></p>
Class for plotting 

1. `plot(self, **kwargs)`:
    - Plot the graph
