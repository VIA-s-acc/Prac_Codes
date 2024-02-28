# PracCodes

## Table Of Content

<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq">Lineq Source</a></em></p>

- [Lineq Classes](#lineq-classes)
    -   [Checker](#checker)
    -   [Generator](#generator)
    -   [Matrix Methods](#matrix-methods)
    -   [Save And Read](#save-and-read)
        -   [Saver](#saver)
        -   [Reader](#reader)


## Lineq Classes 

### Checker
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Checker.py">Checker Source</a></em></p>
This `Checker` class contains three methods:

1. `_signum(num)`: 
   - Calculates the signum of the given number.

2. `_check_solve_web(matrix, b, size, dig, solution, epsilon)`: 
   - Solves a system of linear equations using a web-based matrix calculator.

3. `_sylvesters_criterion(matrix)`: 
   - Checks if the given matrix satisfies Sylvester's criterion for positive definiteness.



### Generator
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Generator.py">Generator Source</a></em></p>

This class Generator contains two static methods:

1. - `generate_random_matrix(size, rng: int = 10, mode: str = None)`:
    - Generates a random matrix of the given size, with an optional mode for symmetric or 3-diagonal matrix.

2. - `generate_random_vector(size, rng: int = 10)`:
    - Generates a random vector of the specified size and range.

### Matrix Methods 
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Matrix_methods.py">Matrix Methods Source</a></em></p>

This class contains methods for various matrix operations:

1. `det(matrix)`: 
    - Calculates the determinant of a square matrix.

2. `LU_decomposition(matrix)`: 
    - Performs LU decomposition on the given matrix and returns the lower and upper triangular matrices.

3. `cholesky_decomposition_v1(matrix)`: 
    - Performs Cholesky decomposition and returns the lower and upper triangular matrices.

4. `cholesky_decomposition_v2(matrix)`: 
    - Performs Cholesky decomposition and returns the lower triangular matrix, diagonal matrix, and upper triangular matrix.

5. `_matrix_multiply(*matrices)`:
    - Performs matrix multiplication on the input matrices and returns the resulting matrix.
    

### Save And Read
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/S_R.py">Save And Read Source</a></em></p>

#### Reader
This `Reader` class has two methods:
1. - `read_matrix_from_file(filename)`: 
    - Reads a matrix from a file and returns a 2D list representing the matrix.
    
2. - `read_vector_from_file(filename)`: 
    - Reads a vector from a file and returns a list containing the integers read from the file.

#### Saver
This class, `Saver`, provides methods to save matrices and vectors to files, and to combine text files into a single output file.

1. - `save_matrix_to_file`: 
    - Saves the given matrix to a file, with an optional 'prettier' mode for formatting.

2. - `save_vector_to_file`: 
    - Saves the given vector to the specified file.

3. - `_combine_txt`: 
    - Combines text files in a specified folder into a single output file, with an option to delete the input text files after combining.

### Prettier
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Lineq/LinEq/Utils/Prettier.py">Prettier Source</a></em></p>

This class, `Prettier`, contains a method `_pretty_matrix` that generates a pretty matrix representation with column labels, row numbers, and proper spacing. 

1. - `_pretty_matrix(matrix)`: 
    - Generates a pretty matrix representation with column labels, row numbers, and proper spacing.





