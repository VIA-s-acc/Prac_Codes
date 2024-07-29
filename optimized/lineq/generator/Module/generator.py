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
    def generate_matrix(size: int, rng: double, mode: string) -> matrix:
        """
        Generate matrix of random numbers
        Args:
            size (int): size of matrix
            rng (int): random number generator ( in generator uses +-1 of min(max). for example: if min is -1 -> real min that used is -2)
            mode (str): mode of matrix
        Returns:
            matrix (list): matrix
        """
        
        return generate_random_matrix(size, rng, mode)

    @staticmethod
    def generate_vector(size: int, rng: double) -> vector:
        """
        Generate vector of random numbers
        Args:
            size (int): size of vector
            rng (int): random number generator ( in generator uses +-1 of min(max). for example: if min is -1 -> real min that used is -2)
        Returns:
            vector (list): vector
        
        """
    
        return generate_random_vector(size, rng)
    
    
    
        