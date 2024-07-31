from ..build.checker import (
    diagonal_domination_pyx,
    symmetric_check_pyx,
    sylvesters_criterion_pyx,
)

from typing import TypeAlias


double: TypeAlias = float
matrix: TypeAlias = list[list[double]]


class Checker():
    """
    Class for matrix checkers
    """
    
    __doc__ = """Checker module\nMethods\n
    diagonal_domination(matrix) -> bool :\t Check matrix diagonal domination
    symmetric_check(matrix) -> bool :\t Check matrix symmetry
    sylvesters_criterion(matrix) -> bool :\t Check matrix sylvesters criterion
    """
    
    version = '0.0.1'
    
    @staticmethod
    def diagonal_domination(matrix: matrix) -> bool:
        """
        Check if a matrix is diagonal dominant.
        
        A matrix is diagonal dominant if the absolute value of its diagonal elements 
        is greater than the sum of absolute values of all other elements on its row and column.
        
        This is a necessary condition for the matrix to be invertible.
        Check matrix diagonal domination
        
        Args:
            matrix (list): 2D list representing a matrix.
        
            matrix (list): matrix 2d 
            
        Returns:
            bool: True if the matrix is diagonal dominant, False otherwise.
        
            bool: True if matrix is diagonal dominant, False otherwise
            
        Example:
        ---
        >>> Checker.diagonal_domination([[1,0],[3,4]])
        True
        
        In this example, the matrix [[1, 0], [3, 4]] is diagonal dominant because the absolute value of its diagonal
        elements (1 and 4) is greater than the sum of absolute values of all other elements on its rows and columns.
        """
        return diagonal_domination_pyx(matrix)
    
    @staticmethod
    def symmetric_check(matrix: matrix) -> bool:
        """
        Check matrix symmetry
        
        This method checks if a matrix is symmetric by comparing each element of the matrix with its corresponding
        element in the transpose of the matrix. If the two elements are equal, the matrix is considered symmetric.
        
        Args:
            matrix (list): matrix 2d 
                
                The matrix to be checked for symmetry. It should be a list of lists, where each inner list represents
                a row in the matrix.
                
            
        Returns:
            bool: True if matrix is symmetric, False otherwise
                
                This method returns True if the matrix is symmetric and False otherwise.
                
            
        Example:
        ---
        >>> Checker.symmetric_check([[1,0],[3,4]])
        False
            
        In this example, the method checks if the matrix [[1,0],[3,4]] is symmetric. Since the matrix is not symmetric
        (i.e., the elements at position (0,0) and (1,1) are not equal), the method returns False.
        """

        return symmetric_check_pyx(matrix)
    
    @staticmethod
    def sylvesters_criterion(matrix: matrix) -> bool:
        """
        Check matrix sylvesters criterion of positive definite
        
        The Sylvester's criterion is a necessary condition for a matrix to be positive definite. It states that a matrix
        A is positive definite if and only if all of its principal minors are positive. In other words, if all the leading
        principal minors of A are positive, then A is positive definite.
        
        Args:
            matrix (list): matrix 2d 
                The matrix to be checked for Sylvester's criterion. It should be a list of lists, where each inner
                list represents a row in the matrix.
                
            
        Returns:
            bool: True if matrix is positive definite, False otherwise
                This method returns True if the matrix is positive definite (i.e., all its principal minors are positive),
                and False otherwise.
                
            bool: True if matrix is sylvesters, False otherwise
            
        Example:
        ---
        >>> Checker.sylvesters_criterion([[1,0],[3,4]])
        True
            In this example, the method checks if the matrix [[1,0],[3,4]] is positive definite. Since all its principal
            minors are positive (i.e., 1 and 4), the method returns True.
        """
        return sylvesters_criterion_pyx(matrix)
   