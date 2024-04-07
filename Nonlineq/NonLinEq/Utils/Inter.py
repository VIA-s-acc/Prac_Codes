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

    - `generate_vandermonde(x)`: generates the Vandermonde matrix
    - `interpolate(func, mode, points, intervals=(0, 1, 10), **kwargs)`: interpolates the function
    - `lagrange_interpolation(x, y, var)`: lagrange interpolation
    - `newton_interpolation(x, y, var)`: newton interpolation
    - `divided_diff(x, y)`: calculates the divided difference table
    - `cspline_interpolation(x, y, x_y_intervals, var)`: cubic spline interpolation

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
    

    def interpolate(func = None, mode: str = 'lagrange', points: str = 'auto', intervals: tuple = (0, 1, 10), **kwargs):
        """
        Interpolates a function using the specified interpolation mode and points.

        Parameters:
            func (function): The function to interpolate.
            - mode (str): The interpolation mode. Defaults to 'lagrange'.
                - modes 
                - lagrange: lagrange interpolation
                - lagrange_vold: lagrange interpolation with vandermonde matrix
                - newton: newton interpolation
                - cspline: cubic spline interpolation ( in cspline intervals[2] is number of splines, work only in auto mode)

            - points (str): The method for determining the interpolation points. Defaults to 'auto'. for manual use 'manual'
                - if 'manual' then points must be a list/tuple of lists/tuples of the form [(x1, y1), (x2, y2), ...] or [[x1, y1], [x2, y2], ...]] or ((x1, y1), (x2, y2), ...) in kwargs['pts']

            - intervals (tuple): The range and number of points for automatically determining the interpolation points. Defaults to (-3, 3, n).| n = 10 -> degree = 10 -> points_num = 11  
                - n (int): n+1 is The number of points. n is the degree of the polynomial.
                        
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
            Polynom: The interpolated polynomial.
        """


        if func is None and points == 'auto':
                raise ValueError('func must be provided when points mode is auto')
            
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
                if mode != 'cspline':
                    x = []
                    y = []
                    start = intervals[0]
                    while start < intervals[1]+step:
                        x.append(start)
                        y.append(func(start))
                        start += step
                elif mode == 'cspline':
                    x = []
                    y = []
                    x_y_intervals = []
                    start = intervals[0]
                    while start < intervals[1]+step:
                        x.append(start)
                        y.append(func(start))
                        if start + step < intervals[1]+step:
                            x_y_intervals.append((start, start+step))
                        start += step

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

        if mode == 'cspline':
            return Interpolation.cspline_interpolation(x, y, x_y_intervals, variable)
             

    def cspline_interpolation(x, y, x_y_intervals, var):
        """
        Cubic spline interpolation

        Args:
            x (list): List of x values
            y (list): List of y values
            x_y_intervals (list): List of intervals
            var (str): Variable of the polynomial

        Returns:
            result (dict): The cubic spline interpolations for each interval in the form of a dictionary
        """       
        result = dict()
        n = len(x_y_intervals)
        h = x_y_intervals[0][1] - x_y_intervals[0][0]
        if n < 2:
            raise ValueError('Not enough points to interpolate | for cubic spline require at least 4 points(2 intervals | intervals[2] must be >= 2)') 
        
        if n == 2:
            c = [0, 6/(4*h**2)*(y[0]-2*y[1]+y[2]), 0]

        if n > 2:
            c = [0]*(n+1)
            F_ = []
            mat_generator = lambda n: [[1 if i == j or i == j + 1 or i + 1 == j else 0 for i in range(n)] for j in range(n)]
            mat = mat_generator(n-1)
            for i in range(n-1):
                mat[i][i] = 4
            for i in range(1, n):
                F_.append( 6/h**2* ( y[i-1]-2*y[i]+y[i+1] ) )
            C_coeffs = LinEqSolver.tridiagonal_elimination(mat, F_, dig = 15)
            for i in range(1, n):
                c[i] = C_coeffs[i-1]

        P = [0]
        Q = [0]
        for i in range(1, n+1):
            P.append(y[i-1] - c[i-1] * (h**2)/6)
            Q.append(y[i] - c[i] * (h**2)/6)

        for i, interval in enumerate(x_y_intervals, 1):
            P1 = c[i-1]/(6*h) * Polynom([[-1, x[i]], var]) * Polynom([[-1, x[i]], var]) * Polynom([[-1, x[i]], var])
            P2 = c[i]/(6*h) * Polynom([[1, -x[i-1]], var]) * Polynom([[1, -x[i-1]], var]) * Polynom([[1, -x[i-1]], var])
            P3 = P[i]/h * Polynom([[-1, x[i]], var])
            P4 = Q[i]/h * Polynom([[1, -x[i-1]], var])
            result[interval] = P1+P2+P3+P4
        
        return result
             

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

    


