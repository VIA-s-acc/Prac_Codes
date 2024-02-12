import unittest
from lineq import LinEqSolver
from tempfile import NamedTemporaryFile
from unittest.mock import patch, mock_open
import lineq

#Default Tests files saving path  "Base/test_files/" <- Create if dont have.

class TestDeterminant(unittest.TestCase):
    def test_2x2_matrix(self):
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(LinEqSolver.det(matrix), -2)

    def test_3x3_matrix(self):
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(LinEqSolver.det(matrix), 0)

    def test_singular_matrix(self):
        matrix = [[0, 0], [0, 0]]
        self.assertEqual(LinEqSolver.det(matrix), 0)

    def test_non_square_matrix(self):
        matrix = [[1, 2, 3], [4, 5, 6]]
        with self.assertRaises(ValueError):
            LinEqSolver.det(matrix)

class TestGaussElimination(unittest.TestCase):

    def test_2x2_unique_solution(self):
        matrix = [[2, 1], [1, -1]]
        vec = [5, -1]
        self.assertEqual(LinEqSolver.gauss_elimination(matrix, vec), [4/3, 7/3])

    def test_3x3_unique_solution(self):
        matrix = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        vec = [8, -11, -3]
        self.assertEqual(LinEqSolver.gauss_elimination(matrix, vec, 0), [2.0, 3.0, -1.0])

    def test_3x3_no_solution(self):
        matrix = [[2, 1, -1], [-3, -1, 2], [-2, -1, 1]]
        vec = [8, -11, 0]
        with self.assertRaises(ValueError):
            LinEqSolver.gauss_elimination(matrix, vec)

    def test_3x3_infinite_solution(self):
        matrix = [[2, 1, -1], [4, 2, -2], [6, 3, -3]]
        vec = [8, 16, 24]
        with self.assertRaises(ValueError):
            LinEqSolver.gauss_elimination(matrix, vec)


class TestGenerateRandomMatrix(unittest.TestCase):

    def test_size_0(self):
        result = LinEqSolver.generate_random_matrix(0)
        self.assertEqual(result, [])

    def test_size_1(self):
        result = LinEqSolver.generate_random_matrix(1)
        self.assertEqual(len(result), 1)
        self.assertTrue(all(isinstance(row, list) and len(row) == 1 for row in result))

    def test_size_5(self):
        result = LinEqSolver.generate_random_matrix(5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(isinstance(row, list) and len(row) == 5 for row in result))


import unittest

class TestSaveMatrixToFile(unittest.TestCase):

    def test_save_3x3_matrix_to_file(self):
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        filename = "test_files/test_matrix.txt"
        LinEqSolver.save_matrix_to_file(matrix, filename)
        with open(filename, 'r') as file:
            content = file.readlines()
            self.assertEqual(content, ["3\n", "1 2 3\n", "4 5 6\n", "7 8 9\n"])

    def test_save_empty_matrix_to_file(self):
        matrix = []
        filename = "test_files/test_empty_matrix.txt"
        LinEqSolver.save_matrix_to_file(matrix, filename)
        with open(filename, 'r') as file:
            content = file.readlines()
            self.assertEqual(content, ["0\n"])

    def test_save_matrix_with_special_characters_to_file(self):
        matrix = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"], ["$", "%", "&"]]
        filename = "test_files/test_special_chars_matrix.txt"
        LinEqSolver.save_matrix_to_file(matrix, filename)
        with open(filename, 'r') as file:
            content = file.readlines()
            self.assertEqual(content, ["4\n", "a b c\n", "d e f\n", "g h i\n", "$ % &\n"])

class TestReadMatrixFromFile(unittest.TestCase):
    
    def test_valid_2x2_matrix(self):
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write('2\n1 2\n3 4\n')
        result = LinEqSolver.read_matrix_from_file(temp_file.name)
        self.assertEqual(result, [[1, 2], [3, 4]])
            
    def test_valid_3x3_matrix(self):
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write('3\n1 2 3\n4 5 6\n7 8 9\n')
        result = LinEqSolver.read_matrix_from_file(temp_file.name)
        self.assertEqual(result, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
    def test_invalid_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            LinEqSolver.read_matrix_from_file('nonexistent_file.txt')
            
    def test_invalid_empty_file(self):
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            pass
        with self.assertRaises(ValueError):
            LinEqSolver.read_matrix_from_file(temp_file.name)


class TestGenerateRandomVector(unittest.TestCase):
    
    def test_positive_size(self):
        size = 5
        result = LinEqSolver.generate_random_vector(size)
        self.assertEqual(len(result), size)
        for num in result:
            self.assertTrue(0 <= num <= 10)
            
    def test_zero_size(self):
        size = 0
        result = LinEqSolver.generate_random_vector(size)
        self.assertEqual(len(result), size)
        
    def test_negative_size(self):
        size = -5
        with self.assertRaises(ValueError):
            LinEqSolver.generate_random_vector(size)
class TestSaveVectorToFile(unittest.TestCase):

    def test_save_empty_vector_to_file(self):
        vector = []
        with NamedTemporaryFile(delete=False) as temp_file:
            filename = temp_file.name
            temp_file.close()  # Explicitly close the file
            LinEqSolver.save_vector_to_file(vector, filename)
            with open(filename, 'r') as file:
                content = file.read()
                self.assertEqual(content, '0\n\n')
                file.close()

    def test_save_non_empty_vector_to_file(self):
        vector = [1, 2, 3, 4, 5]
        with NamedTemporaryFile(delete=False) as temp_file:
            filename = temp_file.name
            temp_file.close()  # Explicitly close the file
            LinEqSolver.save_vector_to_file(vector, filename)
            with open(filename, 'r') as file:
                content = file.read()
                self.assertEqual(content, '5\n1 2 3 4 5\n')
                file.close()

    def test_save_vector_with_negative_numbers_to_file(self):
        vector = [-1, -2, -3, -4, -5]
        with NamedTemporaryFile(delete=False) as temp_file:
            filename = temp_file.name
            temp_file.close()  # Explicitly close the file
            LinEqSolver.save_vector_to_file(vector, filename)
            with open(filename, 'r') as file:
                content = file.read()
                self.assertEqual(content, '5\n-1 -2 -3 -4 -5\n')
                file.close()

class TestReadVectorFromFile(unittest.TestCase):
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='5\n1 2 3 4 5')
    def test_read_vector_with_multiple_integers(self, mock_open):
        result = LinEqSolver.read_vector_from_file('test_file.txt')
        self.assertEqual(result, [1, 2, 3, 4, 5])

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='10\n10')
    def test_read_vector_with_single_integer(self, mock_open):
        result = LinEqSolver.read_vector_from_file('test_file.txt')
        self.assertEqual(result, [10])

    def test_read_vector_from_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            LinEqSolver.read_vector_from_file('nonexistent_file.txt')

# class TestLinearEquations(unittest.TestCase):

#     @patch('builtins.open', new_callable=mock_open)
#     @patch('lineq.LinEqSolver.generate_random_matrix')
#     @patch('lineq.LinEqSolver.generate_random_vector')
#     @patch('lineq.LinEqSolver.gauss_elimination')
#     @patch('lineq.LinEqSolver.save_matrix_to_file')
#     def test_small_matrix_size(self, mock_file, mock_gauss, mock_vector, mock_matrix, mock_open):
#         size = 3
#         matrix_file = "test_matrix_file.txt"
#         vector_file = "test_vector_file.txt"
#         solution_file = "test_solution_file.txt"

#         generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file)

#         mock_matrix.assert_called_once_with(size)
#         mock_vector.assert_called_once_with(size)
#         mock_gauss.assert_called_once_with(mock_matrix.return_value, mock_vector.return_value)
#         mock_open.assert_any_call(matrix_file, 'w')
#         mock_open.assert_any_call(vector_file, 'w')
#         mock_open.assert_any_call(solution_file, 'w')
#         self.assertEqual(mock_file.call_count, 3)

#     @patch('builtins.open', new_callable=mock_open)
#     @patch('lineq.LinEqSolver.generate_random_matrix')
#     @patch('lineq.LinEqSolver.generate_random_vector')
#     @patch('lineq.gauss_elimination')
#     @patch('lineq.LinEqSolver.save_matrix_to_file')
#     def test_large_matrix_size(self, mock_file, mock_gauss, mock_vector, mock_matrix, mock_open):
#         size = 1000
#         matrix_file = "test_matrix_file.txt"
#         vector_file = "test_vector_file.txt"
#         solution_file = "test_solution_file.txt"

#         generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file)

#         mock_matrix.assert_called_once_with(size)
#         mock_vector.assert_called_once_with(size)
#         mock_gauss.assert_called_once_with(mock_matrix.return_value, mock_vector.return_value)
#         mock_open.assert_any_call(matrix_file, 'w')
#         mock_open.assert_any_call(vector_file, 'w')
#         mock_open.assert_any_call(solution_file, 'w')
#         self.assertEqual(mock_file.call_count, 3)


if __name__ == '__main__':
    unittest.main()
