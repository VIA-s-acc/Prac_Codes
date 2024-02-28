from copy import deepcopy

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

class Checker:
    """
    - `_signum(num)`:
    Calculates the signum of the given number.
    - `_check_solve_web(matrix, b, size, dig, solution, epsilon)`:
    Solves a system of linear equations using a web-based matrix calculator.
    - `_sylvesters_criterion(matrix)`: 
    Checks if the given matrix satisfies Sylvester's criterion for positive definiteness.
    """
    def _signum(num):
        """
            Calculate the signum of the given number.

            Parameters:
                num (int): The input number.

            Returns:
                int: The signum of the input number.
        """
        return 1 if num > 0 else -1
    
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
            if det(sub_matrix) <= 0:
                return False
        return True