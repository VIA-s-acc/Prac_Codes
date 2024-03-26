from .Poly import Polynom 
import os 
import sys
import warnings

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Lineq'))
if path not in sys.path:
    sys.path.append(path)

from LinEq import LinEqSolver # import Lineq solver


class Interpolation:
    """
    Interpolates a function using the specified interpolation mode and points.

    - `generate_vandermonde(x)` generates the Vandermonde matrix
    - `interpolate(func, mode, points, intervals=(0, 1, 10), **kwargs)` interpolates the function
    - `lagrange_interpolation(x, y, var)` lagrange interpolation
    - `newton_interpolation(x, y, var)` newton interpolation
    - `divided_diff(x, y)` calculates the divided difference table

    """

    def generate_vandermonde(x):
        """
        Generate the Vandermonde matrix.

        Args:
            x (list): List of x values

        Returns:
            vandermonde (list): List of lists representing the Vandermonde matrix
        """
        n = len(x) 
        vandermonde = []
        for i in range(n):
            vandermonde.append([])
            for j in range(n):
                vandermonde[i].append(x[i]**j)

        return vandermonde
    

    def interpolate(func, mode: str = 'lagrange', points: str = 'auto', intervals: tuple = (0, 1, 10), **kwargs):
        """
        Interpolates a function using the specified interpolation mode and points.

        Parameters:
            func (function): The function to interpolate.
            - mode (str): The interpolation mode. Defaults to 'lagrange'.
                - modes 
                - lagrange: lagrange interpolation
                - lagrange_vold: lagrange interpolation with vandermonde matrix
                - newton: newton interpolation

            - points (str): The method for determining the interpolation points. Defaults to 'auto'. for manual use 'manual'
                - if 'manual' then points must be a list/tuple of lists/tuples of the form [(x1, y1), (x2, y2), ...] or [[x1, y1], [x2, y2], ...]] or ((x1, y1), (x2, y2), ...) in kwargs['pts']

            intervals (tuple): The range and number of points for automatically determining the interpolation points. Defaults to (-3, 3, 10).
            - kwargs: Additional arguments to pass to the interpolation function .
                - lineqmethod (str): The lineq method to use for solving the lineq system. Defaults to 'gauss' if mode is lagrange_vold.
                    - The method list
                    - chol_v1, chol_v2, gauss, lu, thm, iter_sim, iter_sei, iter_jac, iter_rel, iter_exp, iter_minr, iter_std
                    - iter_minc (advanced for minc -> if end by sim, jac or sei, uses specified matrix for minc, see `min_chg_iteration` in `../../Lineq/LinEq/Lineq.py` for more), 
                    - iter_stdi (advanced for stdo -> if end by sim, jac or sei, uses specified matrix for stdi -> see `step_desc_iteration_imp` in `../../Lineq/LinEq/Lineq.py` for more).
                        - for more see `../../Lineq/LinEq/Lineq.py`
                - max_iter (int): The maximum number of iterations. Defaults to 100.
                - eps (float): The tolerance for the bisection method. Defaults to 1e-6.
                - pts (list): The list of points to use for the interpolation. Defaults to None. Need when mode is 'manual'

        Returns:
            None
        """



        if type(func) != type(lambda x: None):
            raise TypeError('func must be a function')
         
        if points == 'auto':
            if type(intervals[2]) != int:
                raise TypeError('Number of points must be an integer')
            
            try:
                step = (intervals[1] - intervals[0]) / intervals[2]
            except:
                raise ValueError('invalid intervals input')
            if intervals:
                x = []
                y = []
                start = intervals[0]
                x.append(start)
                y.append(func(start))
                while start < intervals[1]:
                    start += step
                    x.append(start)
                    y.append(func(start))
                    
            else:
                raise ValueError('Either intervals or points must be provided') 
        if points == 'manual':
            try:
                points = sorted(kwargs['pts'])
                x = [point[0] for point in points]
                y = [point[1] for point in points]

            except:
                raise ValueError('points must be a list/tuple of lists/tuples of the form [(x1, y1), (x2, y2), ...] or [[x1, y1], [x2, y2], ...]] or ((x1, y1), (x2, y2), ...) | incorrect input')
        
        if 'variable' in kwargs.keys():
                variable = kwargs['variable']
        else:
                variable = 'x'
                warnings.warn("variable not specified, using default value of 'x'")
        if mode == 'lagrange_vold':
            if 'lineqmethod' in kwargs.keys():
                if kwargs['lineqmethod'] in ['chol_v1', 'chol_v2', 'gauss', 'lu', 'thm', 'iter_sim', 'iter_sei', 'iter_jac', 'iter_rel', 'iter_exp', 'iter_minr', 'iter_std'] or kwargs['lineqmethod'].startswith('iter_minc') or kwargs['lineqmethod'].startswith('iter_stdi'):
                    lin_mode = kwargs['lineqmethod']
                else:
                    warnings.warn("Warning (Selected method not found): Using default method = 'gauss'")
                    lin_mode = 'gauss'
            else:
                lin_mode = 'gauss'
                warnings.warn("lineqmethod not specified, using default value of 'gauss'")

            if 'max_iter' in kwargs.keys():
                max_iter = kwargs['max_iter']
            else:
                max_iter = 100
                if lin_mode.startswith('iter'):
                    warnings.warn("max_iter not specified, using default value of 100")

            if 'eps' in kwargs.keys():
                eps = kwargs['eps']
            else:
                eps = 1e-6               
                if lin_mode.startswith('iter'):
                    warnings.warn("eps not specified, using default value of 1e-6")
            

            voldemort = Interpolation.generate_vandermonde(x)
            if lin_mode == 'gauss':
                    A = LinEqSolver.gauss_elimination(voldemort, y, 15)
            if lin_mode == 'chol_v1':
                    A,l,u = LinEqSolver._chol_solver(voldemort, y, 15, mode = '1')
            if lin_mode == 'chol_v2':
                    A,l,d,i = LinEqSolver._chol_solver(voldemort, y, 15, mode = '1')
            if lin_mode == 'lu':
                    A,l,u = LinEqSolver._lu_solver(voldemort, y, 15)
            if lin_mode == 'thm':
                    A = LinEqSolver.tridiagonal_elimination(voldemort, y, 15) 
            if lin_mode == 'iter_sim':
                    A = LinEqSolver.simple_iteration(voldemort, y, eigen_max_iter = max_iter, eigen_eps = eps, max_iter = max_iter, eps = eps, dig = 15)
            if lin_mode == 'iter_jac':
                    A = LinEqSolver.jacobi_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15)
            if lin_mode == 'iter_sei':
                    A = LinEqSolver.seidel_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15)
            if lin_mode == 'iter_exp':
                    A = LinEqSolver.explicit_iteration(voldemort, y, eigen_max_iter = max_iter, eigen_eps = eps, max_iter = max_iter, eps = eps, dig = 15) 
            if lin_mode == 'iter_rel':
                    A = LinEqSolver.relaxation_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, omega = LinEqSolver._select_omega(voldemort, eigen_max_iter=max_iter, eigen_eps=eps))
            if lin_mode == 'iter_minr':
                    A = LinEqSolver.min_res_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15) 
            if lin_mode == 'iter_std':
                    A = LinEqSolver.step_desc_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15)
            if lin_mode.startswith('iter_minc'):
                if lin_mode.endswith('sei'):
                    A = LinEqSolver.min_chg_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, matrix_choose_mode = 'sei')
                elif lin_mode.endswith('jac'):
                    A = LinEqSolver.min_chg_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, matrix_choose_mode = 'jac')
                elif lin_mode.endswith('sim'):
                    A = LinEqSolver.min_chg_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, matrix_choose_mode = 'sim')
                else: 
                    A = LinEqSolver.min_chg_iteration(voldemort, y, max_iter = max_iter, eps = eps, dig = 15)
            if lin_mode.startswith('iter_stdi'):
                if lin_mode.endswith('sei'):
                    A = LinEqSolver.step_desc_iteration_imp(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, matrix_choose_mode = 'sei')
                elif lin_mode.endswith('jac'):
                    A = LinEqSolver.step_desc_iteration_imp(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, matrix_choose_mode = 'jac')
                elif lin_mode.endswith('sim'):
                    A = LinEqSolver.step_desc_iteration_imp(voldemort, y, max_iter = max_iter, eps = eps, dig = 15, matrix_choose_mode = 'sim')
                else: 
                    A = LinEqSolver.step_desc_iteration_imp(voldemort, y, max_iter = max_iter, eps = eps, dig = 15)    
   
            return Polynom([A, variable])

        if mode == 'lagrange':
            return Interpolation.lagrange_interpolation(x, y, variable)

        if mode == 'newton':
            return Interpolation.newton_interpolation(x, y, variable)


    def lagrange_interpolation(x, y, var):
        """
        Lagrange interpolation

        Args:
            x (list): List of x values
            y (list): List of y values
            var (str): Variable of the polynomial

        Returns:
            Result (Polynom): The interpolated polynomial
        """
        Result = Polynom([[0], var])
        for k in range(len(x)):
            PLN = Polynom([[1], var])
            for j in range(len(x)):
                if k != j:
                    Poly = 1/(x[k] - x[j]) * Polynom([[1, -x[j]], var])
                    PLN *= Poly
            
            Result += PLN*y[k]
        return Result

                    
                        

    def newton_interpolation(x, y, var):
        """
        Newton interpolation

        Args:
            x (list): List of x values
            y (list): List of y values
            var (str): Variable of the polynomial

        Returns:
            Result (Polynom): The interpolated polynomial
        """
        divided_diff = Interpolation.divided_diff(x, y)
        Result = Polynom([[0], var])
        for i in range(len(x)):
            PLN = Polynom([[1], var])
            for j in range(i):
                PLN *= Polynom([[1, -x[j]], var])

            PLN *= divided_diff[0][i]
            Result += PLN

        return Result 
 
    def divided_diff(x, y):
        """
        Calculate the divided difference table

        Args:
            y (list): List of y values

        Returns:
            table (list): The divided difference table
        """
        
        n = len(x)
        table = [[None for x in range(n-j)] for j in range(n)]

        for i in range(n):
            table[i][0] = float(y[i])

        for j in range(1,n):
            for i in range(n-j):
                try:
                    table[i][j] = (table[i+1][j-1] - table[i][j-1])/(float(x[i+j])-float(x[i]))
                except ZeroDivisionError:
                    table[i][j] = 0

        return table 

    


