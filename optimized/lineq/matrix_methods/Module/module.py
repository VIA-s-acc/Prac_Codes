from ..build.matrix_methods import (
    determinant,
    sum_matrices_wrapper,
    multiply_matrix_by_scalar_wrapper,
    multiply_matrices_wrapper,
    sig,
    absolute,
    random,
    max_matrix,
    inv,
    LU,
    cholv1,
    cholv2,
    eigen,
    power_method,
    norm,
    vec_approx,
)

from .mtypes import (
    double, 
    matrix, 
    vector
)

from .m_err.m_err import (
    BaseMatrixMethodsError, 
    MatrixError, 
    MatrixMethodsError, 
    MatrixShapeError, 
    MatrixValueError
)

import random as rd, sys

class MatrixMethods():
    """Class for matrix methods (multiplication, determinant, sum, decomposition, ...) for all check __doc__"""
    
    version = '0.0.1'
    __doc__ = """MatrixMethods module\nMethods\n---
    \n
    determinant(matrix_a) -> double :\t Returns determinant of matrix_a | API +
    \n
    sum_matrices(matrix_a, matrix_b) -> matrix :\t Returns sum of matrices | API + 
    \n
    multiply_matrix_by_scalar(matrix_a, scalar) -> matrix :\t Returns multiplied matrix | API +
    \n
    multiply_matrices(matrix_a, matrix_b) -> matrix :\t Returns multiplied matrix | API + 
    \n
    sig(x) -> int :\t Returns -1 if x < 0, 0 if x == 0, 1 if x > 0 | API +
    \n
    absolute(x) -> double :\t Returns absolute value of number | API +
    \n
    random(min, max) -> double :\t Returns random number in range (min, max) | API +
    \n
    max_matrix(matrix_a) -> double :\t Returns max value in matrix | API +
    \n
    inverse(matrix_a) -> matrix :\t Returns inverted matrix | API +
    \n
    LU(matrix_a) -> tuple[matrix, matrix] :\t Returns LU decomposition | API +
    \n
    cholv1(matrix_a) -> tuple[matrix, matrix] :\t Returns cholesky decomposition | API +
    \n
    cholv2(matrix_a) -> tuple[matrix, matrix, matrix] :\t Returns cholesky decomposition | API +
    \n
    eigen(matrix_a, max_iter, tol) -> tuple[tuple[double, vector], tuple[double, vector]] :\t Returns eigenvalues and eigenvectors (max, min) | API +
    \n 
    power_method(matrix_a, max_iter, tol) -> tuple[double, vector]:\t Returns eigenvector (iterative method, max) | WIHTOUT API
    \n
    norm(vector) -> double:\t Returns norm (euclidian) | API +
    \n
    vec_approx(vector_a, vector_b) -> bool:\t Returns vector approximation ( True or False ) | API +
    \n
    """
    
    @staticmethod
    def determinant(matrix_a: matrix) -> double:
        """
        Calculate the determinant of a square matrix.

        Args:
            matrix_a (list): A 2D list representing the matrix.

        Returns:
            double: The determinant of the matrix.

        Raises:
            MatrixShapeError: If the matrix is not square.
            MatrixMethodsError: If there is an undefined error in the C module or the matrix is invalid.
        """

        
        if len(matrix_a) != len(matrix_a[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix_a)}x{len(matrix_a[0])}'))
        try:
            return determinant(matrix_a)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
    
    @staticmethod
    def sum_matrices(matrix_a: matrix, matrix_b: matrix) -> matrix:
        """
        Calculate the sum of two matrices.

        Args:
            matrix_a (list): The first matrix.
            matrix_b (list): The second matrix.

        Returns:
            matrix: The sum of the two matrices.

        Raises:
            MatrixShapeError: If the matrices do not have the same shape.
            MatrixMethodsError: If there is an undefined error in the C module or the matrix is invalid.

        Example:
            >>> MatrixMethods.sum_matrices([[1, 0], [3, 4]], [[1, 0], [3, 4]])
            [[2, 0], [6, 8]]
        """
        
        if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
            raise(MatrixShapeError(f'Matrices must have same shape | curr shapes: {len(matrix_a)}x{len(matrix_a[0])} and {len(matrix_b)}x{len(matrix_b[0])}'))
        try:
            return sum_matrices_wrapper(matrix_a, matrix_b)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
        
    @staticmethod
    def multiply_matrix_by_scalar(matrix: matrix, scalar: double) -> matrix:
        """
        Multiply a matrix by a scalar.

        Args:
            matrix (list): A 2D list representing the matrix.
            scalar (float): The scalar to multiply the matrix by.

        Returns:
            matrix: The multiplied matrix.

        Raises:
            MatrixMethodsError: If there is an undefined error in the C module or the matrix is invalid.
        """

        try:
            return multiply_matrix_by_scalar_wrapper(matrix, scalar)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
        
    @staticmethod
    def multiply_matrices(matrix_a: matrix, matrix_b: matrix) -> matrix:
        """
        Multiply two matrices.

        Args:
            matrix_a (list): The first matrix.
            matrix_b (list): The second matrix.

        Returns:
            matrix: The multiplied matrix.

        Raises:
            MatrixShapeError: If the number of columns in matrix_a is not equal to the number of rows in matrix_b.
            MatrixMethodsError: If there is an undefined error in the C module or the matrices are invalid.
        """
        
        if len(matrix_a[0]) != len(matrix_b):
            raise(MatrixShapeError(f'Matrices A columns must be equal to B rows | curr shapes: {len(matrix_a)}x{len(matrix_a[0])} and {len(matrix_b)}x{len(matrix_b[0])}'))
        try:
            return multiply_matrices_wrapper(matrix_a, matrix_b)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
            
    @staticmethod
    def sig(x: double) -> int:
        """
        Signum function
        Returns -1 if x < 0, 0 if x == 0, 1 if x > 0
        
        Args:
            x (float): number
            
        Returns:
            result (float): -1 if x < 0, 0 if x == 0, 1 if x > 0
            
        Example:
        ---
        >>> MatrixMethods.sig(0)
        0
        """
        try:
            return sig(x)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod    
    def absolute(x: double) -> double:
        """
        Absolute value of number
        
        Args:
            x (float): number
            
        Returns:
            result (float): absolute value of number
            
        Example:
        ---
        >>> MatrixMethods.absolute(0)
        0
        """
        try:
            return absolute(x)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module.'))

    @staticmethod
    def random(minv: double, maxv: double) -> double:
        """
        ### ( WORK CORRECT ONLY IN LINUX )
        Generate a random number between the specified minimum and maximum values.

        Args:
            minv (float): The minimum value of the range.
            maxv (float): The maximum value of the range.

        Returns:
            double: The randomly generated number.
        
        Note:
            ~If the platform is Windows, it returns a random number using random.uniform(minv, maxv).~ Base function fixed.
            
        Raises:
            MatrixMethodsError: If an undefined error occurs in the C module.

        Example:
        >>> MatrixMethods.random(0, 10)
        5.2
        """
        # if sys.platform == 'win32':
        #     return rd.uniform(minv, maxv)
        
    
        try:
            return random(minv, maxv)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module.'))

    @staticmethod
    def max_matrix(matrix: matrix) -> double:
        """
        Returns the maximum value in a 2D matrix.

        Args:
            matrix (list): A 2D list representing the matrix.

        Returns:
            double: The maximum value in the matrix.

        Raises:
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is not valid.

        Example:
        >>> MatrixMethods.max_matrix([[1, 2], [3, 4]])
        4
        """
        
        try:
            return max_matrix(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def inverse(matrix: matrix) -> matrix:
        """
        Calculates the inverse of a matrix.

        Args:
            matrix (list): A 2D list representing the matrix.

        Returns:
            matrix: The inverse of the matrix.

        Raises:
            MatrixValueError: If the matrix is singular (determinant is 0).
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.

        Example:
        >>> MatrixMethods.inverse([[1, 2], [3, 4]])
        [[-2.0, 1.0], [1.5, -0.5]]
        """
        
        if determinant(matrix) == 0:
            raise MatrixValueError('Matrix must be non-singular')
        try:
            return inv(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def LU(matrix: matrix) -> tuple[matrix, matrix]:
        """
        Perform LU decomposition on a square matrix.

        Args:
            matrix (list): A 2D list representing the matrix.

        Returns:
            tuple[matrix, matrix]: A tuple containing the L and U matrices of the LU decomposition.

        Raises:
            MatrixShapeError: If the matrix is not square.
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.

        Example:
        >>> MatrixMethods.LU([[1, 0], [3, 4]])
        ([[1.0, 0.0], [0.3333333333333333, 1.0]], [[4.0, 0.0], [0.0, 1.0]])
        """
        
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return LU(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def cholv1(matrix: matrix) -> tuple[matrix, matrix]:
        """
        Perform Cholesky decomposition on a symmetric and positive definite matrix.

        Args:
            matrix (list): A 2D list representing the matrix.

        Returns:
            tuple[matrix, matrix]: A tuple containing the L and U matrices of the Cholesky decomposition.

        Raises:
            MatrixShapeError: If the matrix is not square.
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.

        Example:
            >>> MatrixMethods.cholv1([[1, 0], [3, 4]])
            ([[1.0, 0.0], [0.3333333333333333, 1.0]], [[4.0, 0.0], [0.0, 1.0]])
        """
        
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return cholv1(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def cholv2(matrix: matrix) -> tuple[matrix, matrix, matrix]:
        """
        Perform Cholesky decomposition on a symmetric and positive definite matrix.

        Args:
            matrix (list): A 2D list representing the matrix.

        Returns:
            tuple[matrix, matrix, matrix]: A tuple containing the L, D, and U matrices of the Cholesky decomposition.

        Raises:
            MatrixShapeError: If the matrix is not square.
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.

        Example:
            >>> MatrixMethods.cholv2([[1, 0], [0, 4]])
            ([[1.0, 0.0], [0.0, 2.0]], [[2.0, 0.0], [0.0, 2.0]], [[1.0, 0.0], [0.0, 1.0]])
        """
        
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return cholv2(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def eigen(matrix: matrix, max_iter: int = 100, tol: double = 0.01) -> tuple[tuple[double, vector], tuple[double, vector]]:
        """
        Calculates the eigenvalues and eigenvectors of a square matrix using the power method.

        Args:
            matrix (list): A 2D list representing the square matrix.
            max_iter (int, optional): The maximum number of iterations for the power method. Defaults to 100.
            tol (float, optional): The tolerance for convergence. Defaults to 0.01.

        Returns:
            tuple[tuple[double, vector], tuple[double, vector]]: A tuple containing the eigenvalues and eigenvectors.

        Raises:
            MatrixShapeError: If the matrix is not square.
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.

        Example:
            >>> MatrixMethods.eigen([[1, 0], [0, 4]])
            ((2.0, [0.0, 1.0]), (2.0, [-1.0, 0.0]))
        """
        
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return eigen(matrix, max_iter, tol)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def power_method(matrix: matrix, max_iter: int = 100, tol: double = 0.01) -> tuple[double, vector]:
        """
        Calculates the eigenvalues and eigenvectors of a square matrix using the power method.

        Args:
            matrix (list): A 2D list representing the square matrix.
            max_iter (int, optional): The maximum number of iterations for the power method. Defaults to 100.
            tol (float, optional): The tolerance for convergence. Defaults to 0.01.

        Returns:
            tuple[double, vector]: A tuple containing the eigenvalues and eigenvectors.

        Raises:
            MatrixShapeError: If the matrix is not square.
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.
        """
        
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return power_method(matrix, max_iter, tol)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def norm(vector: vector) -> double:
        """
        Calculate the norm of a vector.

        Args:
            vector (list): A 1D list representing the vector.

        Returns:
            double: The norm of the vector.

        Raises:
            MatrixMethodsError: If an undefined error occurs in the C module or if the matrix is invalid.
        """
        
        try:
            return norm(vector)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
        

    @staticmethod
    def vec_approx(vec_a: vector, vec_b: vector, tol: double = 0.01):
        """
        Approximate vector equality.

        Args:
            vec_a (list): A 1D list representing the first vector.
            vec_b (list): A 1D list representing the second vector.
            tol (float, optional): The tolerance for vector equality. Defaults to 0.01.

        Returns:
            bool: True if the vectors are approximately equal, False otherwise.

        Raises:
            MatrixShapeError: If the vectors do not have the same shape.
            MatrixMethodsError: If there is an undefined error in the C module or if the matrix is invalid.
        """
        
        if len(vec_a) != len(vec_b):
            raise(MatrixShapeError(f'Vectors must be same shape | curr shape: {len(vec_a)}x{len(vec_b)}'))
        try:
            return vec_approx(vec_a, vec_b, tol)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check vectors'))




