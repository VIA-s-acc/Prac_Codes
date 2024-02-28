from copy import deepcopy
import numpy as np
from .Checkers import Checker as Ckr

class Methods:
    """This class contains methods for various matrix operations:

    1. `det(matrix)`: Calculates the determinant of a square matrix.
    2. `LU_decomposition(matrix)`: Performs LU decomposition on the given matrix and returns the lower and upper triangular matrices.
    3. `cholesky_decomposition_v1(matrix)`: Performs Cholesky decomposition and returns the lower and upper triangular matrices.
    4. `cholesky_decomposition_v2(matrix)`: Performs Cholesky decomposition and returns the lower triangular matrix, diagonal matrix, and upper triangular matrix.
    5. `_matrix_multiply(*matrices)`: Performs matrix multiplication on the input matrices and returns the resulting matrix.
    """
    @staticmethod
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