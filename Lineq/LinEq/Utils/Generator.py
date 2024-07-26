import random

class Generator:
    """
    - `generate_random_matrix(size, rng: int = 10, mode: str = None)`:
    Generates a random matrix of the given size, with an optional mode for symmetric or 3-diagonal matrix.
    - `generate_random_vector(size, rng: int = 10)`:
    Generates a random vector of the specified size and range.
    """
    @staticmethod
    def generate_random_matrix(size, rng: int = 10, mode: str = None):
        """
            Generate a random matrix of the given size.
            Args:
                size (int): The size of the matrix.
                rng (int, optional): The range of random values. Defaults to 10.
                mode (str, optional): The mode of the matrix. Either 'symm' for symmetric matrix or None for general matrix or '3diag' for 3-diagonal matrix. Defaults to None.

            Returns:
                list: A 2D list representing the random matrix.
        """
        matrix = []
        if size < 0:
            raise ValueError("Size can't be negative")
        
        if mode is None:
            for _ in range(size):
                row = [random.randint(-rng, rng) for _ in range(size)]
                matrix.append(row)
                
        elif mode == '3diag':
            matrix = [[0] * size for _ in range(size)]
            for i in range(size):
                matrix[i][i] = random.randint(-rng, rng)
                if i > 0:
                    matrix[i][i-1] = random.randint(-rng, rng)
                if i < size-1:
                    matrix[i][i+1] = random.randint(-rng, rng)
                    
        elif mode == "symm":
            matrix = [[0] * size for _ in range(size)]
            for _ in range(size):
                for index in range(_, size):
                    value = random.randint(-rng, rng)
                    matrix[_][index] = value
                    matrix[index][_] = value
        
        return matrix
    
    @staticmethod
    def generate_random_vector(size, rng: int = 10):
        """
            Generate a random vector of the specified size and range.
            
            Args:
                size (int): The size of the vector.
                rng (int, optional): The range of random values. Defaults to 10.
            Returns:
                list: A list of random integers within the specified range.
        """
        if size < 0:
            raise ValueError("Размер не может быть меньше 0")
        return [random.randint(-rng, rng) for _ in range(size)]
    
    