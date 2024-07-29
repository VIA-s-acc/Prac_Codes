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
    def diagonal_domination(matrix) -> bool:
        """
        Check matrix diagonal domination
        
        Args:
            matrix (list): matrix 2d 
            
        Returns:
            bool: True if matrix is diagonal dominant, False otherwise
            
        Example:
        ---
        >>> Checker.diagonal_domination([[1,0],[3,4]])
        True
        """
        return diagonal_domination_pyx(matrix)
    
    @staticmethod
    def symmetric_check(matrix) -> bool:
        """
        Check matrix symmetry
        
        Args:
            matrix (list): matrix 2d 
            
        Returns:
            bool: True if matrix is symmetric, False otherwise
            
        Example:
        ---
        >>> Checker.symmetric_check([[1,0],[3,4]])
        False
        """
        return symmetric_check_pyx(matrix)
    
    @staticmethod
    def sylvesters_criterion(matrix) -> bool:
        """
        Check matrix sylvesters criterion
        
        Args:
            matrix (list): matrix 2d 
            
        Returns:
            bool: True if matrix is sylvesters, False otherwise
            
        Example:
        ---
        >>> Checker.sylvesters_criterion([[1,0],[3,4]])
        True
        """
        return sylvesters_criterion_pyx(matrix)
   