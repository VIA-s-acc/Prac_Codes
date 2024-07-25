from ..build.matrix_methods import \
(
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


from .m_err.m_err import BaseMatrixMethodsError, MatrixError, MatrixMethodsError, MatrixShapeError, MatrixValueError

class MatrixMethods():
    version = '0.0.1'
    __doc__ = """MatrixMethods module\nMethods\n---
    \n
    determinant(matrix_a):\t Returns determinant of matrix_a
    \n
    sum_matrices(matrix_a, matrix_b):\t Returns sum of matrices
    \n
    multiply_matrix_by_scalar(matrix_a, scalar)\t:\t Returns multiplied matrix
    \n
    multiply_matrices(matrix_a, matrix_b):\t Returns multiplied matrix
    \n
    sig(x):\t Returns -1 if x < 0, 0 if x == 0, 1 if x > 0
    \n
    absolute(x):\t Returns absolute value of number
    \n
    random(matrix_a, matrix_b):\t Returns random number in range (min, max)
    \n
    max_matrix(matrix_a):\t Returns max value in matrix
    \n
    inv(matrix_a):\t Returns inverted matrix
    \n
    LU(matrix_a):\t Returns LU decomposition
    \n
    cholv1(matrix_a):\t Returns cholesky decomposition
    \n
    cholv2(matrix_a):\t Returns cholesky decomposition
    \n
    eigen(matrix_a):\t Returns eigenvalues and eigenvectors (max, min)
    \n
    power_method(matrix_a):\t Returns eigenvector (iterative method, max)
    \n
    norm(matrix_a):\t Returns norm (euclidian)
    \n
    vec_approx(matrix_a):\t Returns vector approximation ( True or False )
    \n
    """
    
    @staticmethod
    def determinant(matrix_a):
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
    def sum_matrices(matrix_a, matrix_b):
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
    def multiply_matrix_by_scalar(matrix, scalar):
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
    def multiply_matrices(matrix_a, matrix_b):
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
    def sig(x):
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
    def absolute(x):
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
    def random(minv, maxv):
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
    def max_matrix(matrix):
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
    def inverse(matrix):
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
    def LU(matrix):...

    @staticmethod
    def cholv1(matrix):...

    @staticmethod
    def cholv2(matrix):...

    @staticmethod
    def eigen(matrix, max_iter = 100, tol = 0.01):...

    @staticmethod
    def power_method(matrix, max_iter = 100, tol = 0.01):...

    @staticmethod
    def norm(vector):...

    @staticmethod
    def vec_approx(vec_a, vec_b, tol = 0.01):...


print('Version:', MatrixMethods.version, '\nDocstring:', MatrixMethods.__doc__)

matrix = [[0,1],[3,4]]
matrix2 = [[1,1],[3,4]]
try:
    det = MatrixMethods.determinant(matrix)
    summ = MatrixMethods.sum_matrices(matrix, matrix2)
    mlt = MatrixMethods.multiply_matrix_by_scalar([[1,0],[3,4]],2)
    mlt1 = MatrixMethods.multiply_matrices(matrix, matrix2)
    sig1 = MatrixMethods.sig(1)
    sig0 = MatrixMethods.sig(0)
    sigm1 = MatrixMethods.sig(-1)
    abs1 = MatrixMethods.absolute(1)
    absm1 = MatrixMethods.absolute(-1)
    abs0 = MatrixMethods.absolute(0)
    rand = MatrixMethods.random(0,1)
    maxm = MatrixMethods.max_matrix(matrix)
    inversed = MatrixMethods.inverse(matrix)
    inv_mat = MatrixMethods.multiply_matrices(inversed, matrix)
    print(det, summ, mlt, mlt1, sig1, sig0, sigm1, abs1, absm1, abs0, rand, maxm, inversed, inv_mat)
except Exception as e:
    import traceback
    print(traceback.format_exc())
    
