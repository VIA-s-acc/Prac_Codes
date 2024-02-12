# PracCodes

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gauss</title>
<style>
    body {
        font-family: Arial, sans-serif;
    }

    h3 {
        color: #333;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        margin-bottom: 10px;
    }

    a {
        text-decoration: none;
        color: #007bff;
        transition: color 0.3s ease;
    }

    a:hover {
        color: #0056b3;
    }
</style>
</head>
<body>
<h3>Gauss</h3>
<p><em><a href="https://github.com/VIA-s-acc/Prac_Codes/tree/main/Gauss">Gauss Code</a></em></p>
<ul>
    <li><a href="#Gauss">Gauss Method</a></li>
    <li><a href="#LinEqSolver">LinEqSolver</a></li>
    <li><a href="#Methods">Methods</a></li>
    <li><a href="#Usage">Usage</a></li>
</ul>
</body>
</html>



## Gauss

Gauss Method

### LinEqSolver

The LinEqSolver class provides methods for solving systems of linear equations and working with matrices and vectors.

### Methods:

- `det(matrix):` Calculate the determinant of a square matrix.
- `gauss_elimination(matrix, vec, dig):` Perform Gaussian elimination on the given matrix and vector to solve a system of linear equations.
- `generate_random_matrix(size, range):` Generate a random matrix of the given size.
- `save_matrix_to_file(matrix, filename):` Save the given matrix to a file.
- `read_matrix_from_file(filename):` Read a matrix from a file.
- `generate_random_vector(size, range):` Generate a random vector of the specified size and range.
- `save_vector_to_file(vector, filename):` Save the given vector to the specified file.
- `read_vector_from_file(filename):` Read a vector from the given file.
- `_check_solve_web(matrix, b, size, dig, solution, epsilon):` Solve a system of linear equations using a web-based matrix calculator.
- `generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig, check, epsilon, m_v_range):` Generate and solve a system of linear equations.

### Usage:

```python
from LinEqSolver import LinEqSolver

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
