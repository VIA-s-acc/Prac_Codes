import os
from .Prettier import Prettier as Prt
class Saver:
    """    
    This class, `Saver`, provides methods to save matrices and vectors to files, and to combine text files into a single output file.

    - `save_matrix_to_file`: Saves the given matrix to a file, with an optional 'prettier' mode for formatting.
    - `save_vector_to_file`: Saves the given vector to the specified file.
    - `_combine_txt`: Combines text files in a specified folder into a single output file, with an option to delete the input text files after combining.
    """
    def save_matrix_to_file(matrix, filename, mode = None):
        """
            Save the given matrix to a file.

            Args:
                matrix (list): The matrix to be saved to the file.
                filename (str): The name of the file to which the matrix will be saved.
                mode (str, optional): The mode of the matrix. Either 'prettier' or None. Defaults to None.
            Returns:
                None
        """

        if mode == "prettier":
            if not isinstance(matrix, str):
                matrix = Prt._pretty_matrix(matrix)
            with open(filename, 'w') as file:
                file.write(matrix)

        else:
            with open(filename, 'w') as file:
                size = len(matrix)
                file.write(f"{size}\n")
                for row in matrix:
                    file.write(' '.join(map(str, row)) + '\n')

    def save_vector_to_file(vector, filename):
        """
            Save the given vector to the specified file.

            Args:
                vector: The vector to be saved to the file.
                filename: The name of the file to which the vector will be saved.
        """
        with open(filename, 'w') as file:
            size = len(vector)
            file.write(f"{size}\n")
            file.write(' '.join(map(str, vector)) + '\n')

    def _combine_txt(folder_path, output_file, delete_flag=False):  
        """
        Combine the text files in the specified folder into a single output file.

        Args:
            folder_path (str): The path to the folder containing the text files.
            output_file (str): The path to the output file to write the combined content to.
            delete_flag (bool, optional): Whether to delete the input text files after combining. Defaults to False.
        """
        import os
        files = []
        with open(output_file, 'w') as combined_file:
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    combined_file.write(f"{filename}\n\n")
                    filepath = os.path.join(folder_path, filename)
                    files.append(filepath)
                    with open(filepath, 'r') as file:
                        combined_file.write(file.read())
                        combined_file.write("\n\n")
        try:
            files.remove(output_file)        
        except:...
        if delete_flag:
            for filepath in files:
                os.remove(filepath)



class Reader:
    """   
    This `Reader` class has two methods:
    1. `read_matrix_from_file(filename)`: Reads a matrix from a file and returns a 2D list representing the matrix.
    2. `read_vector_from_file(filename)`: Reads a vector from a file and returns a list containing the integers read from the file.
    """
    def read_matrix_from_file(filename):
        """
            Read a matrix from a file.

            Args:
                filename (str): The name of the file to read the matrix from.

            Returns:
                list: A 2D list representing the matrix read from the file.
        """
        with open(filename, 'r') as file:
            size = int(file.readline().strip())
            matrix = []
            for _ in range(size):
                row = list(map(int, file.readline().strip().split()))
                matrix.append(row)
        return matrix
    

    def read_vector_from_file(filename):
        """
            Read a vector from the given file.

            Args:
                filename (str): The name of the file to read from.

            Returns:
                list: A list containing the integers read from the file.
        """
        with open(filename, 'r') as file:
            size = int(file.readline().strip())
            vector = list(map(int, file.readline().strip().split()))
        return vector