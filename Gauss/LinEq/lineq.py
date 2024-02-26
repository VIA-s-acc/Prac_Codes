from copy import deepcopy 
import random 
import numpy as np
import time 

def time_decorator(func):
    """
    A decorator function that measures the execution time of the input function and prints the time taken. 
    Takes in a function as input and returns a wrapper function. 
    """
    def wrapper(*args, **kwargs):
        """
        This function acts as a wrapper for another function, timing its execution and printing the duration. 
        It takes any number of positional and keyword arguments and returns the result of the wrapped function. 
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper



class LinEqSolver():
    """
    This class definition is for a linear equation solver using Gaussian elimination. Here's what each class method does:

    det(matrix): Calculates the determinant of a square matrix.
    gauss_elimination(matrix, vec, dig): Performs Gaussian elimination to solve a system of linear equations.
    generate_random_matrix(size, rng, mode): Generates a random matrix of the given size.
    save_matrix_to_file(matrix, filename): Saves the given matrix to a file.
    read_matrix_from_file(filename): Reads a matrix from a file.
    generate_random_vector(size, rng): Generates a random vector of the specified size and range.
    save_vector_to_file(vector, filename): Saves the given vector to a file.
    read_vector_from_file(filename): Reads a vector from a file.
    _check_solve_web(matrix, b, size, dig, solution, epsilon): Solves a system of linear equations using a web-based matrix calculator and checks the solution.
    LU_decomposition(matrix): Performs LU decomposition on the given matrix.
    _signum(num): Calculates the signum of the given number.
    cholesky_decomposition_v2(matrix): Performs Cholesky decomposition on the given matrix.
    _sylvesters_criterion(matrix): Checks if the given matrix satisfies Sylvester's criterion for positive definiteness.
    cholesky_decomposition_v1(matrix): Performs Cholesky decomposition on the given matrix.
    _matrix_multiply(*matrices): Performs matrix multiplication on the input matrices.
    _chol_solver(matrix, vec, dig, mode): Solves a linear system using Cholesky decomposition or LU decomposition.
    _lu_solver(matrix, vec, dig): Solves a linear system of equations using LU decomposition.
    _forward_substitution(matrix, vec, dig): Solves a system of linear equations using forward substitution.
    _backward_substitution(matrix, vec, dig): Solves a system of linear equations using backward substitution.
    generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig, check, epsilon, m_v_range, mode, random, **kwargs): Generates and solves a system of linear equations, with options for different solving methods and file saving options.
    """
    @staticmethod
    def det(matrix):
        """
        Calculate the determinant of a square matrix.

        Args:
            matrix: The input square matrix.

        Returns:
            float: The determinant of the input matrix.
        """
        A = deepcopy(matrix)
        n = len(A)
        if n != len(A[0]):
            raise ValueError("The matrix must be square.")

        det = 1
        for i in range(n):

            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k

            det *= A[i][i]

            for k in range(i+1, n):
                if A[i][i] != 0:
                    factor = -A[k][i] / A[i][i]
                    for j in range(i+1, n):
                        A[k][j] += factor * A[i][j]
        return det
    

    @staticmethod 
    def gauss_elimination(matrix, vec, dig: int = -1):
        """
            Performs Gaussian elimination on the given matrix and vector to solve a system of linear equations.
            
            Args:
                matrix: The matrix representing the coefficients of the linear equations.
                vec: The vector representing the constants of the linear equations.
                dig (int, optional): The number of digits to round the solution to. Defaults to 0.
            
            Returns:
                list: The solution to the system of linear equations.
        """
        if dig < 0:
            return ValueError('digits-nums < 0')
        A = deepcopy(matrix)
        b = deepcopy(vec)
        n = len(b)
        try: 
            A[0]
        except:
            raise ValueError("Size can't be 0")
    
        det = LinEqSolver.det(matrix)

        if n != len(A[0]):
            raise ValueError("Vector and matrix sizes do not match.")
        
        if det == 0:
            raise ValueError("The matrix is singular.")

        test_matrix = deepcopy(A)
        for i in range(n):
            test_matrix[i].append(b[i])

        for i in range(n):

            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k

            if i != max_row:
                A[i], A[max_row] = A[max_row], A[i]
                b[i], b[max_row] = b[max_row], b[i]

            pivot = A[i][i]

            for j in range(i, n):
                A[i][j] /= pivot
            b[i] /= pivot

            for j in range(i + 1, n):
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
        del A
        del b
        x = [round(el, dig) for el in x]

        return x
    


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
            raise ValueError("Размер не может быть меньше 0")
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
            print(matrix)
            with open(filename, 'w') as file:
                file.write(matrix)

        else:
            with open(filename, 'w') as file:
                size = len(matrix)
                file.write(f"{size}\n")
                for row in matrix:
                    file.write(' '.join(map(str, row)) + '\n')


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
    

    def _check_solve_web(matrix, b, size, dig, solution, epsilon):
        """
            Function to solve a system of linear equations using a web-based matrix calculator.
        
            Args:
                matrix: The matrix of coefficients of the linear equations.
                b: The matrix of constant terms in the linear equations.
                size: The size of the matrix.
                dig: The number of decimal places to consider in the solution.
                solution: The expected solution to the system of linear equations.
                epsilon: The tolerance for the maximum difference between the expected and calculated solution.
            
            Returns:
                parsed_list: The parsed list of solutions obtained from the web calculator.
                sub_result: The detailed comparison between the expected and calculated solution, along with the maximum difference and decision outcome.
        """
        from selenium import webdriver
        import time
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import re

        matrix_str = []
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://matrixcalc.org/slu.html")
        time.sleep(1)
        button = driver.find_element(By.CLASS_NAME, "swap-mode-button")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "swap-mode-button")))
        button.click()
        textarea = driver.find_element(By.CLASS_NAME,"matrix-table-textarea")
        for i in range(size):
            matrix_str.append(matrix[i]+[b[i]])
        text = '\n'.join([' '.join(map(str, row)) for row in matrix_str])
        textarea.clear()  
        textarea.send_keys(text)  
        check_button = driver.find_element(By.ID, "decfraccheckbox")
        check_button.click()
        dig_inp = driver.find_element(By.ID, "frdigits")
        dig_inp.clear()
        if dig >= 0:
            dig_inp.send_keys(str(dig))
        send_button  = driver.find_element(By.XPATH,"//button[text()='Solve']")
        send_button.click()
        time.sleep(3)
        element = driver.find_element(By.CLASS_NAME, "list-unstyled")
        formatting = element.text.split()
        formatting = [el.replace('−', '-') for el in formatting]
        flag = True
        i = 0
        while flag:
            try:
                formatting[i+1] 
                if formatting[i] == '=':
                    if formatting[i+1] != '-':
                        formatting.insert(i+1, '+')
                i += 1
            except:
                flag = False
        formatting_len = len(formatting)
        parsed_list = []
        for i in range(0, formatting_len, 5):
            if i+4 < formatting_len:
                parsed_list.append(f'{formatting[i]}{formatting[i+1]} {formatting[i+2]} {formatting[i+3]}{formatting[i+4]}')
        driver.quit()
        checking_result = []
        for i in parsed_list:
            elem = float(i[5::].replace(',', '.'))
            checking_result.append((elem))
        sub_result = []
        sub_val = [abs(i-k) for i,k in zip(checking_result, solution)]
        for i,k in zip(solution, checking_result):
            sub_result.append(f'|{str(i)} - {str(k)}'.rjust(5) + f'| = {str(abs(i-k))}'.ljust(5))
        sub_result.append(f"Max: {max(sub_val)}")
        if max(sub_val) < epsilon:
            sub_result.append(f"\nSuccessful, the decision is correct!")
        else:
            sub_result.append("\nFailure, the decision is wrong!")
        return parsed_list, sub_result
    

    def LU_decomposition(matrix):
        """
        Perform LU decomposition on the given matrix.

        Parameters:
        matrix (list of lists): The input matrix for LU decomposition.

        Returns:
        tuple: A tuple containing the lower and upper triangular matrices resulting from the decomposition.
        """
        n = len(matrix)
        lower = [[0] * n for _ in range(n)]
        upper = [[0] * n for _ in range(n)]
        if LinEqSolver.det(matrix) == 0:
            raise ValueError("The matrix is singular")
        for i in range(n):
            lower[i][i] = 1

            for j in range(i, n):
                sum = 0
                for k in range(i):
                    sum += (lower[i][k] * upper[k][j])

                upper[i][j] = matrix[i][j] - sum

            for j in range(i, n):
                sum = 0
                for k in range(i):
                    sum += (lower[j][k] * upper[k][i])

                lower[j][i] = (matrix[j][i] - sum) / upper[i][i]

        return lower, upper
    
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

        col_labels = " " * 10 + "|"+" "*(max) + f"|{" "*max}".join(f"Col {i}" for i in range(1, num_cols + 1)) + ' |'

        separator = "-" * (len(col_labels) + 2)
        result += f"{separator}\n{col_labels}\n{separator}"

        for i, row in enumerate(matrix):
            row_str = f"Row {i+1: <5} |" + "|".join(map(lambda x: f"{x: > {max+5}}", row)) + " |"
            result += f"\n{row_str}"
        result += "\n" + separator
        return result


    def _signum(num):
        """
            Calculate the signum of the given number.

            Parameters:
                num (int): The input number.

            Returns:
                int: The signum of the input number.
        """
        return 1 if num > 0 else -1
    
    def cholesky_decomposition_v2(matrix):
        """
            Performs Cholesky decomposition on the given matrix.

            Args:
                matrix: The input matrix for Cholesky decomposition.

            Returns:
                lower: The lower triangular matrix from the decomposition.
                diagonal_matrix: The diagonal matrix from the decomposition.
                upper: The upper triangular matrix from the decomposition.
        """
        size = len(matrix)
        upper = [[0] * size for _ in range(size)]
        diagonal = [0] * size
        for i in range(size):
            for j in range(i, size):
                if i == j:
                    sum_v =  matrix[i][i] - sum(diagonal[k]*upper[k][i]**2 for k in range(i))
                    diagonal[i] = LinEqSolver._signum(sum_v)
                    upper[i][i] = np.sqrt(abs(sum_v))
                else:
                    sum_v = (matrix[i][j] - sum(upper[k][i]*upper[k][j]*diagonal[k] for k in range(i)))/(upper[i][i]*diagonal[i])
                    upper[i][j] = sum_v
        
        
        m_g = lambda vec: [[vec[i] if i == j else 0 for j in range(len(vec))] for i in range(len(vec))]
        lower = [[upper[j][i] for j in range(len(upper))] for i in range(len(upper[0]))]
        return lower, m_g(diagonal), upper

    

    def _sylvesters_criterion(matrix):
        """
            Check if the given matrix satisfies Sylvester's criterion for positive definiteness.

            Args:
                matrix: The input matrix to be checked.

            Returns:
                True if the matrix satisfies Sylvester's criterion for positive definiteness, False otherwise.
        """
        n = len(matrix)
        for i in range(1, n + 1):
            sub_matrix = [row[:i] for row in matrix[:i]]
            if LinEqSolver.det(sub_matrix) <= 0:
                return False
        return True

    def cholesky_decomposition_v1(matrix):
        """
            Performs Cholesky decomposition on the given matrix.

            Args:
                matrix: The input matrix for Cholesky decomposition.

            Returns:
                lower: The lower triangular matrix of the decomposition.
                upper: The upper triangular matrix of the decomposition.
        """

        size = len(matrix)
        lower = [[0] * size for _ in range(size)]
        upper = [[0] * size for _ in range(size)]

        for i in range(size):
            for j in range(i+1):
                if i == j:
                    lower[i][j] = np.sqrt(matrix[i][i] - sum(lower[i][k] ** 2 for k in range(j))) 
                    upper[j][i] = lower[i][j]
                else:
                    lower[i][j] = (1.0 / lower[j][j] * (matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))))
                    upper[j][i] = lower[i][j]

        return lower, upper
    def _matrix_multiply(*matrices):
        """
            Perform matrix multiplication on the input matrices and return the resulting matrix.
        """
        result = matrices[0]
        for matrix in matrices[1:]:
            result = [[sum(a * b for a, b in zip(row_x, col_y)) for col_y in zip(*matrix)] for row_x in result]
        return result

    def _chol_solver(matrix, vec, dig = 1, mode = '1'):
        """
            Solve a linear system using Cholesky decomposition.

            Args:
                matrix: The matrix of the linear system.
                vec: The vector of the linear system.
                mode: The mode of Cholesky decomposition. Default is '1'.

            Returns:
                Tuple: Depending on the mode, it returns different values.
                    If mode is '1', returns x, lower, and upper.
                    If mode is '2', returns x, lower, diagonal, and upper.
        """
        
        if mode == '1':
            if LinEqSolver._sylvesters_criterion(matrix):
                lower, upper = LinEqSolver.cholesky_decomposition_v1(matrix)
                y = LinEqSolver._forward_substitution(lower, vec, dig=dig)
            else:
                raise ValueError("Sylvester's criterion not satisfied.")
        elif mode == '2':
            lower, diagonal, upper = LinEqSolver.cholesky_decomposition_v2(matrix)            
            lower_upd = LinEqSolver._matrix_multiply(lower, diagonal)
            y = LinEqSolver._forward_substitution(lower_upd, vec, dig=dig)

        x = LinEqSolver._backward_substitution(upper, y, dig=dig)
        if mode == '1':
            return x, lower, upper
        elif mode == '2':
            return x, lower, diagonal, upper

    

    def _lu_solver(matrix, vec, dig:int = 1):
        """
            Solves a linear system of equations using LU decomposition.
            
            Args:
                matrix: The coefficient matrix of the linear system.
                vec: The vector of constants in the linear system.
                dig: The number of digits to round the solution to (default is 1).
            
            Returns:
                x: The solution vector.
                lower: The lower triangular matrix from the LU decomposition.
                upper: The upper triangular matrix from the LU decomposition.
        """ 
        
        if dig < 0:
            dig = 0
        lower, upper = LinEqSolver.LU_decomposition(matrix)
        y = LinEqSolver._forward_substitution(lower,vec, dig)
        x = LinEqSolver._backward_substitution(upper, y, dig)
        return x, lower, upper


    def _forward_substitution(matrix, vec, dig):
        """
            Solve a system of linear equations using forward substitution.
        """
        size = len(matrix)  
        y = [0] * size
        y[0] = vec[0] / matrix[0][0]
        for i in range(1, size):
            y[i] = round((vec[i] - sum(matrix[i][j] * y[j] for j in range(i))) / matrix[i][i], dig)
        return y
    
    def _backward_substitution(matrix, vec, dig):
        """
            Solve a system of linear equations using backward substitution.
        """
        size = len(matrix)
        x = [0] * size
        x[-1] = vec[-1] / matrix[-1][-1]
        for i in range(size - 1, -1, -1):
            x[i] = round((vec[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, size))) / matrix[i][i],dig)
        return x
    

    @time_decorator
    def generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig: int = 0, check: bool = False, epsilon = 1e-5, m_v_range: tuple = (10,10), mode: str = 'gauss', random = True,prettier_path = None, prettier = False, **kwargs):
        """
            Generate and solve a system of linear equations.
            
            Args:
                size (int): The size of the matrix and vector.
                matrix_file (str): The file to save the generated matrix.
                vector_file (str): The file to save the generated vector.
                solution_file (str): The file to save the solution to the linear equations.
                ext_file (bool): Flag to determine if an external file should be saved.
                dig (int, optional): The number of decimal places for the solution. Defaults to 0.
                check (bool, optional): Flag to enable checking the solution. Defaults to False.
                epsilon (float): The acceptable margin of error for the solution. Defaults to 1e-5.
                m_v_range (tuple): The range for generating random matrix and vector values. Defaults to (10, 10).
                mode (str): The method to use for solving the linear equations. Defaults to 'gauss'. method list 'chol_v1, chol_v2, gauss, lu'
                random (bool): Flag to determine if the matrix and vector should be generated randomly. Defaults to True.
                prettier_path (str): The path to the prettier executable. Defaults to None.
                prettier (bool): Flag to enable prettier output. Defaults to False.
                **kwargs: if random is False, the matrix and vector should be provided as kwargs with keys 'matrix' and 'vector'.
            Returns:
                None
        """
        if random:
            if mode == 'chol_v1' or mode == 'chol_v2':
                matrix = LinEqSolver.generate_random_matrix(size, m_v_range[0], mode = 'symm')
            else:
                matrix = LinEqSolver.generate_random_matrix(size, m_v_range[0])
            vector = LinEqSolver.generate_random_vector(size, m_v_range[1])
        else:
            try:
                matrix = kwargs['matrix']
                vector = kwargs['vector']
            except:
                raise ValueError("Matrix and vector must be provided as kwargs with keys 'matrix' and 'vector' in random = False mode.")
            size = len(kwargs['matrix'])
            check_matrix_size = lambda size, matrix: all(len(row) == size for row in matrix)
            if not check_matrix_size(len(kwargs['matrix'][0]), kwargs['matrix']):
                raise ValueError("The matrix is not a square matrix.")
        d_f = lambda x: x if x > 0 else 0
        dig = d_f(dig)
        LinEqSolver.save_matrix_to_file(matrix, matrix_file)
        LinEqSolver.save_vector_to_file(vector, vector_file)
        if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(matrix), prettier_path+'matrix.txt', mode = 'prettier')
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix([[i] for i in vector]), prettier_path+'vector.txt', mode = 'prettier')

        if mode == 'gauss':
                solution = LinEqSolver.gauss_elimination(matrix, vector, dig)
        if mode == 'chol_v1':
                solution,lower,upper = LinEqSolver._chol_solver(matrix, vector, dig, mode = '1')
                lower = [list(map(lambda x: round(x, dig), row)) for row in lower]
                upper = [list(map(lambda x: round(x, dig), row)) for row in upper]
                LinEqSolver.save_matrix_to_file(lower, matrix_file+'_chol_L.txt')
                LinEqSolver.save_matrix_to_file(upper, matrix_file+'_chol_U.txt')
                if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(lower), prettier_path+'_chol_L.txt', mode = 'prettier')
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(upper), prettier_path+'_chol_U.txt', mode = 'prettier')
        
        if mode == 'chol_v2':
                solution,lower,diagonal,upper = LinEqSolver._chol_solver(matrix, vector, dig, mode = '2')
                lower = [list(map(lambda x: round(x, dig), row)) for row in lower]
                upper = [list(map(lambda x: round(x, dig), row)) for row in upper]
                LinEqSolver.save_matrix_to_file(lower, matrix_file+'_chol_dec_L.txt')
                LinEqSolver.save_matrix_to_file(upper, matrix_file+'_chol_dec_U.txt')
                LinEqSolver.save_matrix_to_file(diagonal, matrix_file+'_chol_dec_D.txt')
                if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(lower), prettier_path+'_chol_dec_L.txt', mode = 'prettier')
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(upper), prettier_path+'_chol_dec_U.txt', mode = 'prettier')
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(diagonal), prettier_path+'_chol_dec_D.txt', mode = 'prettier')

        if mode == 'lu':
                solution,lower,upper = LinEqSolver._lu_solver(matrix, vector, dig)
                LinEqSolver.save_matrix_to_file(lower, matrix_file+'_lu_L.txt')
                LinEqSolver.save_matrix_to_file(upper, matrix_file+'_lu_U.txt')
                if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(lower), prettier_path+'_lu_L.txt', mode = 'prettier')
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix(upper), prettier_path+'_lu_U.txt', mode = 'prettier')
                
        if ext_file:
            sol_eq = [[]] * size
            
            for i in range(size):
                sol_eq[i] = ['|'] + [str(x).rjust(3) for x in matrix[i]] + ['|', '* |', str(solution[i]).rjust(7) + ' | ->', str(vector[i]).rjust(4).ljust(4)]
            if check:
                if dig >= 0:
                    check_res, sub_result = LinEqSolver._check_solve_web(matrix, vector, size, dig, solution, epsilon)
                else:
                    check_res, sub_result = LinEqSolver._check_solve_web(matrix, vector, size, dig, solution=solution, epsilon=epsilon)
                
                sol_eq.extend(["Checker_Mode: ON\n",f"Epsilon: {epsilon}\n","Program_Result:\n"] + [f"x{i+1} = {solution[i]}" for i in range(len(solution))] + ['\n'] + ['Checker_Result:\n'] + check_res + ['\n'] + ['Cheking:\n'] + sub_result)
            else:
                sol_eq.extend([" ","Checker_Mode: OFF"])
            LinEqSolver.save_matrix_to_file(sol_eq, ext_file)

        if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    LinEqSolver.save_matrix_to_file(LinEqSolver._pretty_matrix([[i] for i in solution]), prettier_path+'solution.txt', mode = 'prettier')
        LinEqSolver.save_vector_to_file(solution, solution_file)
