from copy import deepcopy
import numpy as np
import random
from .Checkers import Checker as Ckr
import warnings
class Methods:
    """This class contains methods for various matrix operations:

    1. `det(matrix)`: Calculates the determinant of a square matrix.
    2. `LU_decomposition(matrix)`: Performs LU decomposition on the given matrix and returns the lower and upper triangular matrices.
    3. `cholesky_decomposition_v1(matrix)`: Performs Cholesky decomposition and returns the lower and upper triangular matrices.
    4. `cholesky_decomposition_v2(matrix)`: Performs Cholesky decomposition and returns the lower triangular matrix, diagonal matrix, and upper triangular matrix.
    5. `_matrix_multiply(*matrices)`: Performs matrix multiplication on the input matrices and returns the resulting matrix.
    6. `euclidean_norm(vector)`: Calculates the Euclidean norm of a vector.
    7. `_scalar_matrix_multiply(scalar, matrix)`: Performs matrix multiplication on the input matrices and returns the resulting matrix.
    8. `_vector_matrix_multiply(matrix, vector)`: Multiply a matrix by a vector and return the resulting vector.
    9. `_vector_approximation(v1, v2, tol=1e-6)`: Check if two vectors are approximately equal within a tolerance.
    10. `_inverse_matrix(matrix)`: Calculate the inverse of a matrix using Gauss-Jordan elimination.
    11. `eigen_get(matrix, max_iter=100, eps=1e-6)`: Calculate the eigenvalues and eigenvectors of the given matrix using the power method algorithm.
    12. `power_method(matrix, max_iter=100, eps=1e-6)`: Perform the power method to find the dominant eigenvalue and eigenvector of the given matrix.
    13. `eigen_get(matrix, max_iter=100, eps=1e-6)`: Calculate the max_min eigenvalues and eigenvectors of the given matrix using the power method algorithm.
    """

    def euclidean_norm(vector):
        """
        Calculate the Euclidean norm of a vector.

        Args:
            vector: The input vector.   

        Returns:
            float: The Euclidean norm of the input vector.  
        """
        return (sum(x**2 for x in vector))**0.5

    def _vector_approximation(v1, v2, tol=1e-6):
        """
        Check if two vectors are approximately equal within a tolerance.

        Args:
            v1 (list): The first vector.
            v2 (list): The second vector.
            tol (float): The tolerance level for approximation. Defaults to 1e-6.

        Returns:
            bool: True if vectors are approximately equal, False otherwise.
        """
        if len(v1) != len(v2):
            return False
        return Methods.euclidean_norm([a-b for a,b in zip(v1,v2)])<tol


    def _inverse_matrix(matrix):
        """
        Calculate the inverse of a matrix using Gauss-Jordan elimination.

        Args:
            matrix (list of list of float): The input matrix.

        Returns:
            list of list of float: The inverse of the input matrix, if it exists.
            None: If the matrix is not invertible.
        """

        n = len(matrix)
        mat = deepcopy(matrix)
        inv_mat = [[float(i == j) for j in range(n)] for i in range(n)]

        for i in range(n):
            diag = mat[i][i]
            if diag == 0:
                for k in range(i+1, n):
                    if mat[k][i] != 0:
                        mat[i], mat[k] = mat[k], mat[i]
                        inv_mat[i], inv_mat[k] = inv_mat[k], inv_mat[i]
                        break
                else:
                    return None
                diag = mat[i][i]
            for j in range(n):
                mat[i][j] /= diag
                inv_mat[i][j] /= diag

            for k in range(n):
                if k != i:
                    factor = mat[k][i]
                    for j in range(n):
                        mat[k][j] -= factor * mat[i][j]
                        inv_mat[k][j] -= factor * inv_mat[i][j]

        return inv_mat

    def eigen_get(matrix, max_iter: int = 100, eps: float = 1e-6):
        """
        Calculate the eigenvalues and eigenvectors of the given matrix using the power method algorithm.
        
        Args:
            matrix: The input matrix for which eigenvalues and eigenvectors are to be computed.
            max_iter (int): The maximum number of iterations for the power method. Defaults to 100.
            eps (float): The convergence criterion. Defaults to 1e-6.
        
        Returns:
            tuple: A tuple containing the maximum eigenvalue and its corresponding eigenvector,
                   and another tuple containing the minimum eigenvalue and its corresponding eigenvector.
        """
        
        max_eigen, max_vec = Methods._power_method(matrix, max_iter, eps)
        E = [[1 if i == j else 0 for i in range(len(matrix))] for j in range(len(matrix[0]))]
        transform_matrix = lambda m, s, e: [[m[i][j] - s * e[i][j] for j in range(len(m))] for i in range(len(m))]
        B = transform_matrix(matrix, max_eigen, E)

        min_eigen, min_vec = Methods._power_method(B, max_iter, eps)
        
        if max_eigen > 0:
            min_eigen = max_eigen + min_eigen
        if max_eigen < 0:
            temp = min_eigen
            min_eigen = max_eigen
            max_eigen = max_eigen + temp 

        return (max_eigen, max_vec), (min_eigen, min_vec)

    def _power_method(matrix, max_iter: int = 100, eps: float = 1e-6):
        """
        Perform the power method to find the dominant eigenvalue and eigenvector of the given matrix.

        Args:
            matrix: The input matrix for which the dominant eigenvalue and eigenvector are to be found.
            max_iter: The maximum number of iterations to perform (default is 100).
            eps: The tolerance for convergence (default is 1e-6).

        Returns:
            Tuple containing the dominant eigenvalue and its corresponding eigenvector.
        """     
        max_v = max(map(lambda row: max(row), matrix))
        start_vector = [random.uniform(0, max_v+1) for _ in range(len(matrix))]
        norm = Methods.euclidean_norm(start_vector)
        start_vector = [element / norm for element in start_vector] 
        for _ in range(max_iter):
            eigenvalue = Methods._vector_matrix_multiply([[x] for x in start_vector], (Methods._vector_matrix_multiply(matrix, vector=start_vector)))
            norm = Methods._vector_matrix_multiply([[x] for x in start_vector], start_vector)[0]
            eigenvalue = eigenvalue[0]/norm
            new_vector = (Methods._matrix_multiply(matrix, [[x] for x in start_vector]))
            new_vector = [x[0] for x in new_vector]
            new_norm = Methods.euclidean_norm(new_vector)
            try:
                new_vector = [element / new_norm for element in new_vector]
            except:
                warnings.warn("Power method did not converge, returned last eigenvalue and vector (increase max_iter or decrease eps)")
                return eigenvalue, start_vector
            
            new_eigenvalue = Methods._vector_matrix_multiply([[x] for x in new_vector], (Methods._vector_matrix_multiply(matrix, vector=new_vector)))
            new_norm = Methods._vector_matrix_multiply([[x] for x in new_vector], new_vector)[0]
            new_eigenvalue = new_eigenvalue[0]/new_norm
            if abs(new_eigenvalue-eigenvalue) < eps:
                return new_eigenvalue, new_vector
            else:
                start_vector = new_vector
        warnings.warn("Power method did not converge, returned last eigenvalue and vector (increase max_iter or decrease eps)")
        return eigenvalue, new_vector

        


            
            



    def det(matrix):
        """
        Calculate the determinant of a square matrix.

        Args:
            matrix: The input square matrix.

        Returns:
            float: The determinant of the input matrix.
        """
        A = deepcopy(matrix)
        n = len(A)
        if n != len(A[0]):
            raise ValueError("The matrix must be square.")

        det = 1
        for i in range(n):

            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k

            det *= A[i][i]

            for k in range(i+1, n):
                if A[i][i] != 0:
                    factor = -A[k][i] / A[i][i]
                    for j in range(i+1, n):
                        A[k][j] += factor * A[i][j]
        return det
    

    def LU_decomposition(matrix):
        """
        Perform LU decomposition on the given matrix.

        Parameters:
        matrix (list of lists): The input matrix for LU decomposition.

        Returns:
        tuple: A tuple containing the lower and upper triangular matrices resulting from the decomposition.
        """
        n = len(matrix)
        lower = [[0] * n for _ in range(n)]
        upper = [[0] * n for _ in range(n)]
        if Methods.det(matrix) == 0:
            raise ValueError("The matrix is singular")
        for i in range(n):
            lower[i][i] = 1

            for j in range(i, n):
                sum = 0
                for k in range(i):
                    sum += (lower[i][k] * upper[k][j])

                upper[i][j] = matrix[i][j] - sum

            for j in range(i, n):
                sum = 0
                for k in range(i):
                    sum += (lower[j][k] * upper[k][i])

                lower[j][i] = (matrix[j][i] - sum) / upper[i][i]

        return lower, upper
    

    def cholesky_decomposition_v1(matrix):
        """
            Performs Cholesky decomposition on the given matrix.

            Args:
                matrix: The input matrix for Cholesky decomposition.

            Returns:
                lower: The lower triangular matrix of the decomposition.
                upper: The upper triangular matrix of the decomposition.
        """

        size = len(matrix)
        lower = [[0] * size for _ in range(size)]
        upper = [[0] * size for _ in range(size)]

        for i in range(size):
            for j in range(i+1):
                if i == j:
                    lower[i][j] = np.sqrt(matrix[i][i] - sum(lower[i][k] ** 2 for k in range(j))) 
                    upper[j][i] = lower[i][j]
                else:
                    lower[i][j] = (1.0 / lower[j][j] * (matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))))
                    upper[j][i] = lower[i][j]

        return lower, upper
    

    def cholesky_decomposition_v2(matrix):
        """
            Performs Cholesky decomposition on the given matrix.

            Args:
                matrix: The input matrix for Cholesky decomposition.

            Returns:
                lower: The lower triangular matrix from the decomposition.
                diagonal_matrix: The diagonal matrix from the decomposition.
                upper: The upper triangular matrix from the decomposition.
        """
        size = len(matrix)
        upper = [[0] * size for _ in range(size)]
        diagonal = [0] * size
        for i in range(size):
            for j in range(i, size):
                if i == j:
                    sum_v =  matrix[i][i] - sum(diagonal[k]*upper[k][i]**2 for k in range(i))
                    diagonal[i] = Ckr._signum(sum_v)
                    upper[i][i] = np.sqrt(abs(sum_v))
                else:
                    sum_v = (matrix[i][j] - sum(upper[k][i]*upper[k][j]*diagonal[k] for k in range(i)))/(upper[i][i]*diagonal[i])
                    upper[i][j] = sum_v
        
        
        m_g = lambda vec: [[vec[i] if i == j else 0 for j in range(len(vec))] for i in range(len(vec))]
        lower = [[upper[j][i] for j in range(len(upper))] for i in range(len(upper[0]))]
        return lower, m_g(diagonal), upper
    

    def _matrix_multiply(*matrices):
        """
            Perform matrix multiplication on the input matrices and return the resulting matrix.
        """
        result = matrices[0]
        for matrix in matrices[1:]:
            result = [[sum(a * b for a, b in zip(row_x, col_y)) for col_y in zip(*matrix)] for row_x in result]
        return result
    
    def _scalar_matrix_multiply(scalar, matrix):
        """
            Perform matrix multiplication on the input matrices and return the resulting matrix.

        Args:

            scalar (float): The scalar to multiply with.
            matrix (list of lists): The matrix to multiply.

        Returns:

            list of lists: The resulting matrix.

        """
        return [[scalar * element for element in row] for row in matrix]
    
    
    def _vector_matrix_multiply(matrix, vector):
        """
            Multiply a matrix and a vector
        
        Args:
            matrix (list of lists): The matrix to multiply.
            vector (list): The vector to multiply.

        Returns:
            list: The resulting vector.
        """
        result = []
        for i in range(len(matrix[0])):
            column_sum = sum(vector[j] * matrix[j][i] for j in range(len(vector)))
            result.append(column_sum)
        return result

