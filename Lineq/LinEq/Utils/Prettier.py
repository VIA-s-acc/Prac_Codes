class Prettier:
    """
    This class, `Prettier`, contains a method `_pretty_matrix` that generates a pretty matrix representation with column labels, row numbers, and proper spacing. 

    - `_pretty_matrix(matrix)`: Generates a pretty matrix representation with column labels, row numbers, and proper spacing.
    """
    def _pretty_matrix(matrix):
        """
            Generates a pretty matrix representation with column labels, row numbers, and proper spacing.
            
            Args:
                matrix (list of lists): The input matrix.

            Returns:
                str: The pretty matrix representation.
        """
        max = 0
        for row in matrix:
            for element in row:
                if max < len(str(element)):
                    max = len(str(element))
        num_cols = len(matrix[0])
        num_rows = len(matrix)
        result = ""

        col_labels = " " * 10 + "|" + f"|".join(f"{f"Col {i}": >{max+4}} " for i in range(1, num_cols + 1)) + ' |'

        separator = "-" * (len(col_labels) + 2)
        result += f"{separator}\n{col_labels}\n{separator}"

        for i, row in enumerate(matrix):
            row_str = f"Row {i+1: <5} |" + "|".join(map(lambda x: f"{x: > {max+5}}", row)) + " |"
            result += f"\n{row_str}"
        result += "\n" + separator
        return result