from .Utils.Generator import Generator as Gn
from .Utils.S_R import Saver as Sv
from .Utils.S_R import Reader as Rd
from .Utils.timer import time_decorator
from .Utils.Matrix_methods import Methods as MM
from .Utils.Checkers import Checker as Ckr
from .Utils.Prettier import Prettier as Prt
import numpy as np
from copy import deepcopy


class LinEqSolver():
    """
    This class is a linear equation solver that provides methods for performing various operations related to solving systems of linear equations. Here's a brief summary of each class method:

    gauss_elimination(matrix, vec, dig): Performs Gaussian elimination to solve a system of linear equations.
    _chol_solver(matrix, vec, dig, mode): Solves a linear system using Cholesky decomposition.
    _lu_solver(matrix, vec, dig): Solves a linear system of equations using LU decomposition.
    _forward_substitution(matrix, vec, dig): Solves a system of linear equations using forward substitution.
    _backward_substitution(matrix, vec, dig): Solves a system of linear equations using backward substitution.
    generate_and_solve_linear_equations(size, matrix_file, vector_file, solution_file, ext_file, dig, check, epsilon, m_v_range, mode, random, prettier_path, prettier, **kwargs): Generates and solves a system of linear equations, with various options for customization and output.
    """
    

    

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
    
        det = MM.det(matrix)

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
            if Ckr._sylvesters_criterion(matrix):
                lower, upper = MM.cholesky_decomposition_v1(matrix)
                y = LinEqSolver._forward_substitution(lower, vec, dig=dig)
            else:
                raise ValueError("Sylvester's criterion not satisfied.")
        elif mode == '2':
            lower, diagonal, upper = MM.cholesky_decomposition_v2(matrix)            
            lower_upd = MM._matrix_multiply(lower, diagonal)
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
        lower, upper = MM.LU_decomposition(matrix)
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
                matrix = Gn.generate_random_matrix(size, m_v_range[0], mode = 'symm')
            else:
                matrix = Gn.generate_random_matrix(size, m_v_range[0])
            vector = Gn.generate_random_vector(size, m_v_range[1])
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
        Sv.save_matrix_to_file(matrix, matrix_file)
        Sv.save_vector_to_file(vector, vector_file)
        if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    Sv.save_matrix_to_file(Prt._pretty_matrix(matrix), prettier_path+'matrix.txt', mode = 'prettier')
                    Sv.save_matrix_to_file(Prt._pretty_matrix([[i] for i in vector]), prettier_path+'vector.txt', mode = 'prettier')

        if mode == 'gauss':
                solution = LinEqSolver.gauss_elimination(matrix, vector, dig)
        if mode == 'chol_v1':
                solution,lower,upper = LinEqSolver._chol_solver(matrix, vector, dig, mode = '1')
                lower = [list(map(lambda x: round(x, dig), row)) for row in lower]
                upper = [list(map(lambda x: round(x, dig), row)) for row in upper]
                Sv.save_matrix_to_file(lower, matrix_file+'_chol_L.txt')
                Sv.save_matrix_to_file(upper, matrix_file+'_chol_U.txt')
                if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    Sv.save_matrix_to_file(Prt._pretty_matrix(lower), prettier_path+'_chol_L.txt', mode = 'prettier')
                    Sv.save_matrix_to_file(Prt._pretty_matrix(upper), prettier_path+'_chol_U.txt', mode = 'prettier')
        
        if mode == 'chol_v2':
                solution,lower,diagonal,upper = LinEqSolver._chol_solver(matrix, vector, dig, mode = '2')
                lower = [list(map(lambda x: round(x, dig), row)) for row in lower]
                upper = [list(map(lambda x: round(x, dig), row)) for row in upper]
                Sv.save_matrix_to_file(lower, matrix_file+'_chol_dec_L.txt')
                Sv.save_matrix_to_file(upper, matrix_file+'_chol_dec_U.txt')
                Sv.save_matrix_to_file(diagonal, matrix_file+'_chol_dec_D.txt')
                if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    Sv.save_matrix_to_file(Prt._pretty_matrix(lower), prettier_path+'_chol_dec_L.txt', mode = 'prettier')
                    Sv.save_matrix_to_file(Prt._pretty_matrix(upper), prettier_path+'_chol_dec_U.txt', mode = 'prettier')
                    Sv.save_matrix_to_file(Prt._pretty_matrix(diagonal), prettier_path+'_chol_dec_D.txt', mode = 'prettier')

        if mode == 'lu':
                solution,lower,upper = LinEqSolver._lu_solver(matrix, vector, dig)
                lower = [list(map(lambda x: round(x, dig), row)) for row in lower]
                upper = [list(map(lambda x: round(x, dig), row)) for row in upper]
                Sv.save_matrix_to_file(lower, matrix_file+'_lu_L.txt')
                Sv.save_matrix_to_file(upper, matrix_file+'_lu_U.txt')
                if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    Sv.save_matrix_to_file(Prt._pretty_matrix(lower), prettier_path+'_lu_L.txt', mode = 'prettier')
                    Sv.save_matrix_to_file(Prt._pretty_matrix(upper), prettier_path+'_lu_U.txt', mode = 'prettier')
                
        if ext_file:
            sol_eq = [[]] * size
            
            for i in range(size):
                sol_eq[i] = ['|'] + [str(x).rjust(3) for x in matrix[i]] + ['|', '* |', str(solution[i]).rjust(7) + ' | ->', str(vector[i]).rjust(4).ljust(4)]
            if check:
                if dig >= 0:
                    check_res, sub_result = Ckr._check_solve_web(matrix, vector, size, dig, solution, epsilon)
                else:
                    check_res, sub_result = Ckr._check_solve_web(matrix, vector, size, dig, solution=solution, epsilon=epsilon)
                
                sol_eq.extend(["Checker_Mode: ON\n",f"Epsilon: {epsilon}\n","Program_Result:\n"] + [f"x{i+1} = {solution[i]}" for i in range(len(solution))] + ['\n'] + ['Checker_Result:\n'] + check_res + ['\n'] + ['Cheking:\n'] + sub_result)
            else:
                sol_eq.extend([" ","Checker_Mode: OFF"])
            Sv.save_matrix_to_file(sol_eq, ext_file)

        if prettier:
                    if not prettier_path:
                        raise ValueError("Please provide the path to the prettier executable.")
                    Sv.save_matrix_to_file(Prt._pretty_matrix([[i] for i in solution]), prettier_path+'solution.txt', mode = 'prettier')
        Sv.save_vector_to_file(solution, solution_file)