from ..build.generator import (
    generate_random_matrix,
    generate_random_vector
)

from typing import TypeAlias


double: TypeAlias = float
matrix: TypeAlias = list[list[double]]
vector: TypeAlias = list[double]
string: TypeAlias = str

class Generator():
    """Class for matrix and vector generation"""
    
    __doc__ = """Generator module\nMethods\n
    generate_matrix(size: int, rng: double, mode: string) -> matrix :\t Generate matrix of random numbers ( modes -> 'else': random, '3diag': three diagonal, 'symm': symmetric )
    generate_vector(size: int, rng: double) -> vector: \t Generate vector of random numbers
    """
    
    version = '0.0.1'
    
    
    @staticmethod
    def generate_matrix(size: int, rng: double, mode: string = 'else') -> matrix:
        """
        Generate matrix of random numbers
        Args:
            size (int): size of matrix
            rng (int): random number generator  
            mode (str): mode of matrix 
                - `3diag`: three diagonal
                - `symm`: symmetric
                - `else`: random
        Returns:
            matrix (list): matrix
        """
        
        return generate_random_matrix(size, rng, mode)

    @staticmethod
    def generate_vector(size: int, rng: double) -> vector:
        """
        Generate vector of random numbers
        
        This method generates a vector of random numbers of given size.
        The random numbers are generated using the given range (rng).
        The range is used to generate numbers in the range min(rng) - max(rng).
        For example, if the range is (-1, 1), the generated numbers will be
        between -1 and 1.
        
        Args:
            size (int): size of vector
            rng (float): random number generator

        Returns:
            vector (list): vector of random numbers
        
        Example:
        >>> generator.Generator.generate_vector(5, (-1, 1))
        [-0.5123123123123, 0.98723123123123, -0.23123123123123, 0.123123123123123, 0.87654321]
        """
    
        return generate_random_vector(size, rng)
    
    
    
        