from copy import deepcopy 
import random 
import numpy as np

class LinEqSolver():
    """
    The LinEqSolver class provides methods for solving systems of linear equations and working with matrices and vectors.

    Methods:
    - `det(matrix):` Calculate the determinant of a square matrix.
    - `gauss_elimination(matrix, vec, dig):` Perform Gaussian elimination on the given matrix and vector to solve a system of linear equations.
    - `generate_random_matrix(size, range):` Generate a random matrix of the given size.
    - `save_matrix_to_file(matrix, filename):` Save the given matrix to a file.
    - `read_matrix_from_file(filename):` Read a matrix from a file.
    - `generate_random_vector(size, range):` Generate a random vector of the specified size and range.
    - `save_vector_to_file(vector, filename):` Save the given vector to the specified file.
    - `read_vector_from_file(filename):` Read a vector from the given file.
    - `_check_solve_web(matrix, b, size, dig, solution, epsilon):` Solve a system of linear equations using a web-based matrix calculator.
    - `generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig, check, epsilon, m_v_range):` Generate and solve a system of linear equations.
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
            raise ValueError("Матрица должна быть квадратной")

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
                dig (int, optional): The number of digits to round the solution to. Defaults to -1.
            
            Returns:
                list: The solution to the system of linear equations.
        """

        A = deepcopy(matrix)
        b = deepcopy(vec)
        n = len(b)
        try: 
            A[0]
        except:
            raise ValueError("Размер не может быть 0")
    
        det = LinEqSolver.det(matrix)

        if n != len(A[0]):
            raise ValueError("Матрица должна быть квадратной.")
        
        if det == 0:
            raise ValueError("Бесконечное количество решений.")

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
        if dig != -1:
            temp = [round(el, dig) for el in x]
            x = temp
            del temp
        return x
    

    def generate_random_matrix(size, rng: int = 10):
        """
            Generate a random matrix of the given size.
            Args:
                size (int): The size of the matrix.
                rng (int, optional): The range of random values. Defaults to 10.

            Returns:
                list: A 2D list representing the random matrix.
        """
        matrix = []
        if size < 0:
            raise ValueError("Размер не может быть меньше 0")
        
        for _ in range(size):
            row = [random.randint(-rng, rng) for _ in range(size)]
            matrix.append(row)
        return matrix
    
    def save_matrix_to_file(matrix, filename):
        """
            Save the given matrix to a file.

            Args:
                matrix (list): The matrix to be saved to the file.
                filename (str): The name of the file to which the matrix will be saved.

            Returns:
                None
        """
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
        time.sleep(1)
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

    def generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig: int = -1, check: bool = False, epsilon = 1e-5, m_v_range: tuple = (10,10)):
        """
            Generate and solve a system of linear equations.
            
            Args:
                size (int): The size of the matrix and vector.
                matrix_file (str): The file to save the generated matrix.
                vector_file (str): The file to save the generated vector.
                solution_file (str): The file to save the solution to the linear equations.
                ext_file (bool): Flag to determine if an external file should be saved.
                dig (int, optional): The number of decimal places for the solution. Defaults to -1.
                check (bool, optional): Flag to enable checking the solution. Defaults to False.
                epsilon (float): The acceptable margin of error for the solution. Defaults to 1e-5.
                m_v_range (tuple): The range for generating random matrix and vector values. Defaults to (10, 10).
            
            Returns:
                None
        """
        matrix = LinEqSolver.generate_random_matrix(size, m_v_range[0])
        vector = LinEqSolver.generate_random_vector(size, m_v_range[1])
        if dig >= 0:
            solution = LinEqSolver.gauss_elimination(matrix, vector, dig=dig)
        else:
            check_res = LinEqSolver._check_solve_web(matrix, vector, size, dig)
            solution = LinEqSolver.gauss_elimination(matrix, vector)
        if ext_file:
            sol_eq = [[]] * size
            for i in range(size):
                sol_eq[i] = ['|'] + [str(x).rjust(3) for x in matrix[i]] + ['|', '* |', str(solution[i]).rjust(7) + ' | ->', str(vector[i]).rjust(4).ljust(4)]
            if check:
                if dig >= 0:
                    check_res, sub_result = LinEqSolver._check_solve_web(matrix, vector, size, dig, solution, epsilon)
                else:
                    check_res, sub_result = LinEqSolver._check_solve_web(matrix, vector, size, solution=solution, epsilon=epsilon)
                
                sol_eq.extend(["Checker_Mode: ON\n",f"Epsilon: {epsilon}\n","Program_Result:\n"] + [f"x{i} = {solution[i]}" for i in range(len(solution))] + ['\n'] + ['Checker_Result:\n'] + check_res + ['\n'] + ['Cheking:\n'] + sub_result)
            else:
                sol_eq.extend([" ","Checker_Mode: OFF"])
            LinEqSolver.save_matrix_to_file(sol_eq, ext_file)

        LinEqSolver.save_matrix_to_file(matrix, matrix_file)
        LinEqSolver.save_vector_to_file(vector, vector_file)
        LinEqSolver.save_vector_to_file(solution, solution_file)
