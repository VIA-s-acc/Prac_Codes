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


class MatrixMethods():
    """Class for matrix methods (multiplication, determinant, sum, decomposition, ...) for all check __doc__"""
    
    version = '0.0.1'
    __doc__ = """MatrixMethods module\nMethods\n---
    \n
    determinant(matrix_a) -> double :\t Returns determinant of matrix_a
    \n
    sum_matrices(matrix_a, matrix_b) -> matrix :\t Returns sum of matrices
    \n
    multiply_matrix_by_scalar(matrix_a, scalar) -> matrix :\t Returns multiplied matrix
    \n
    multiply_matrices(matrix_a, matrix_b) -> matrix :\t Returns multiplied matrix
    \n
    sig(x) -> int :\t Returns -1 if x < 0, 0 if x == 0, 1 if x > 0
    \n
    absolute(x) -> double :\t Returns absolute value of number
    \n
    random(matrix_a, matrix_b) -> double :\t Returns random number in range (min, max)
    \n
    max_matrix(matrix_a) -> double :\t Returns max value in matrix
    \n
    inv(matrix_a) -> matrix :\t Returns inverted matrix
    \n
    LU(matrix_a) -> tuple[matrix, matrix] :\t Returns LU decomposition
    \n
    cholv1(matrix_a) -> tuple[matrix, matrix] :\t Returns cholesky decomposition
    \n
    cholv2(matrix_a) -> tuple[matrix, matrix, matrix] :\t Returns cholesky decomposition
    \n
    eigen(matrix_a) -> tuple[tuple[double, vector], tuple[double, vector]] :\t Returns eigenvalues and eigenvectors (max, min)
    \n
    power_method(matrix_a) -> tuple[double, vector]:\t Returns eigenvector (iterative method, max)
    \n
    norm(matrix_a) -> double:\t Returns norm (euclidian)
    \n
    vec_approx(matrix_a) -> bool:\t Returns vector approximation ( True or False )
    \n
    """
    
    @staticmethod
    def determinant(matrix_a) -> double:
        """
        Determinant of matrix 
        
        Args:
            matrix_a (list): matrix 2d
            
        Returns:
            result (float): determinant of matrix
        
        Example:
        ---
        >>> MatrixMethods.determinant([[1,0],[3,4]])
        """
        
        if len(matrix_a) != len(matrix_a[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix_a)}x{len(matrix_a[0])}'))
        try:
            return determinant(matrix_a)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
    
    @staticmethod
    def sum_matrices(matrix_a, matrix_b) -> matrix:
        """
        Sum of matrices
        
        Args:
            matrix_a (list): matrix 2d
            matrix_b (list): matrix 2d
            
        Returns:
            result (list): sum of matrices
        
        Example:
        ---
        >>> MatrixMethods.sum_matrices([[1,0],[3,4]],[[1,0],[3,4]])
        """
        if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
            raise(MatrixShapeError(f'Matrices must have same shape | curr shapes: {len(matrix_a)}x{len(matrix_a[0])} and {len(matrix_b)}x{len(matrix_b[0])}'))
        try:
            return sum_matrices_wrapper(matrix_a, matrix_b)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
        
    @staticmethod
    def multiply_matrix_by_scalar(matrix, scalar) -> matrix:
        """
        Multiply matrix by scalar
        
        Args:
            matrix (list): matrix 2d
            scalar (float): scalar
            
        Returns:
            result (list): multiplied matrix
        
        Example:
        ---
        >>> MatrixMethods.multiply_matrix_by_scalar([[1,0],[3,4]],[[1,0],[3,4]])
        """
        try:
            return multiply_matrix_by_scalar_wrapper(matrix, scalar)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
        
    @staticmethod
    def multiply_matrices(matrix_a, matrix_b) -> matrix:
        """
        Multiply matrices
        
        Args:
            matrix_a (list): matrix 2d
            matrix_b (list): matrix 2d
            
        Returns:
            result (list): multiplied matrix
        
        Example:
        ---
        >>> MatrixMethods.multiply_matrices([[1,0],[3,4]],[[1,0],[3,4]])
        """
        if len(matrix_a[0]) != len(matrix_b):
            raise(MatrixShapeError(f'Matrices A columns must be equal to B rows | curr shapes: {len(matrix_a)}x{len(matrix_a[0])} and {len(matrix_b)}x{len(matrix_b[0])}'))
        try:
            return multiply_matrices_wrapper(matrix_a, matrix_b)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
            
    @staticmethod
    def sig(x) -> int:
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
    def absolute(x) -> double:
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
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def random(minv, maxv) -> double:
        """
        Random number generator
        
        Args:
            minv (float): min value
            maxv (float): max value
            
        Returns:
            result (float): random number ( very low precision )
            
        Example:
        ---
        >>> MatrixMethods.random(0,10)
        """
        try:
            return random(minv, maxv)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def max_matrix(matrix) -> double:
        """
        Max value in matrix
        
        Args:
            matrix (list): matrix 2d
            
        Returns:
            result (float): max value in matrix
            
        Example:
        ---
        >>> MatrixMethods.max_matrix([[1,0],[3,4]])
        4
        """
        try:
            return max_matrix(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def inverse(matrix) -> matrix:
        """
        Inverse matrix
        
        Args:
            matrix (list): matrix 2d
            
        Returns:
            result (list): inverse matrix
            
        Example:
        ---
        >>> MatrixMethods.inv([[1,0],[3,4]])
        """
        if determinant(matrix) == 0:
            raise MatrixValueError('Matrix must be non-singular')
        try:
            return inv(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def LU(matrix) -> tuple[matrix, matrix]:
        """
        LU decomposition \\
        A = LU
        
        Args:
            matrix (list): matrix 2d
            
        Returns:
            result (tuple): LU decomposition L and U Matrices (L, U)
            
        Example:
        ---
        >>> MatrixMethods.LU([[1,0],[3,4]])
        """
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return LU(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def cholv1(matrix) -> tuple[matrix, matrix]:
        """
        Cholesky decomposition \\
        A = LL^T
        
        Args:
            matrix (list): matrix 2d ( symmetric and positive definite )
            
        Returns:
            result (tuple): Cholesky decomposition CL and CU matrices (CL, CU)
            
        Warning:
        ---
        Cholesky decomposition is only for symmetric positive definite matrices
        If you want, you can write checker for that.
        
        Example:
        ---
        >>> MatrixMethods.cholv1([[1,0],[3,4]])
        """
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return cholv1(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def cholv2(matrix) -> tuple[matrix, matrix, matrix]:
        """
        Cholesky decomposition \\
        A = LDL^T
        
        Args:
            matrix (list): matrix 2d ( symmetric and positive definite )
            
        Returns:
            result (tuple): Cholesky decomposition CL, CD, CU matrices (CL, CD, CU)
            
        Warning:
        ---
        Cholesky decomposition is only for symmetric positive definite matrices
        If you want, you can write checker for that.
        
        Example:
        ---
        >>> MatrixMethods.cholv2([[1,0],[3,4]])
        """
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return cholv2(matrix)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def eigen(matrix, max_iter = 100, tol = 0.01) -> tuple[tuple[double, vector], tuple[double, vector]]:
        """
        Eigenvalues and eigenvectors
        
        Args:
            matrix (list): matrix 2d
            max_iter (int): max number of iterations
            tol (float): tolerance
            
        Returns:
            result (tuple): eigenvalues and eigenvectors
            
        Example:
        ---
        >>> MatrixMethods.eigen([[1,0],[3,4]])
        """
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return eigen(matrix, max_iter, tol)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def power_method(matrix, max_iter = 100, tol = 0.01) -> tuple[double, vector]:
        """
        Power method
        
        Args:
            matrix (list): matrix 2d
            max_iter (int): max number of iterations
            tol (float): tolerance
            
        Returns:
            result (tuple): eigenvalues and eigenvectors (res_maxvalue, res_maxvector)
            
        Example:
        ---
        >>> MatrixMethods.power_method([[1,0],[3,4]])
        """
        if len(matrix) != len(matrix[0]):
            raise(MatrixShapeError(f'Matrix must be square | curr shape: {len(matrix)}x{len(matrix[0])}'))
        try:
            return power_method(matrix, max_iter, tol)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))

    @staticmethod
    def norm(vector) -> double:
        """
        Norm of vector
        
        Args:
            vector (list): vector 1d
            
        Returns:
            result (float): norm of vector
            
        Example:
        ---
        >>> MatrixMethods.norm([1,2,3])
        """
        try:
            return norm(vector)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))
        

    @staticmethod
    def vec_approx(vec_a, vec_b, tol = 0.01):
        """
        Approximate vector equality
        
        Args:
            vec_a (list): vector 1d
            vec_b (list): vector 1d
            tol (float): tolerance
            
        Returns:
            result (bool): vector equality
            
        Example:
        ---
        >>> MatrixMethods.vec_approx([1,2,3], [1,2,3])
        """
        if len(vec_a) != len(vec_b):
            raise(MatrixShapeError(f'Vectors must be same shape | curr shape: {len(vec_a)}x{len(vec_b)}'))
        try:
            return vec_approx(vec_a, vec_b, tol)
        except:
            raise(MatrixMethodsError('Undefined error | in .C module. | Check matrix'))



def matmult(a, b):
    if len(a[0]) != len(b):
        raise ValueError("The number of columns in the first matrix must be equal to the number of rows in the second matrix")
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
                
    return result


