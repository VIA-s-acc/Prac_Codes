import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Lineq'))
if path not in sys.path:
    sys.path.append(path)

from LinEq import LinEqSolver # import Lineq solver

class MPE():
    """
    Class for solving MPE
    dy/dx = f(t, y) 
    y(x0) = y0

    f must be function of x,y
    Example:
    -------
    def f(x,y):
        return -x+y
    """
    def __init__(self, Area: tuple, f, f0):
        """
            Class for solving MPE

            Args:
                Area (tuple): Domain of the equation
                f (function): Right side of the equation
                f0 (float): Initial function value
        """ 
        if type(f) == type(lambda x: None):
            self.f = f
        else:
            raise TypeError('f must be a function')
        self.Area = Area
        self.f0 = f0
        self.x = []


    def eiler(self, n):
        """
            Eiler method

        Args:
            n (int): Number of steps
        """
        theta = (self.Area[1]-self.Area[0])/n
        result = [self.f0]
        self.x = [self.Area[0]+theta*i for i in range(n)]
        for i in range(1, n):
            result.append(result[i-1] + theta*self.f(self.Area[0]+(i)*theta, result[i-1]))
        return result
    
    def heun(self, n):
        """
            Heun method
        Args:
            n (int): Number of steps
        """

        theta = (self.Area[1] - self.Area[0])/n
        y_ = self.eiler(n)
        result = [self.f0]
        self.x = [self.Area[0]+theta*i for i in range(n)]
        for i in range(1, n):
            result.append(y_[i-1] + theta/2*(self.f(self.Area[0]+(i-1)*theta, result[i-1]) + self.f(self.Area[0]+i*theta, y_[i])))
        return result

    
    def k_step_Adams_explicit(k, ret_str: bool = False):
        """Build K step Adams explicit method а  

        Formula:
        ---
        y_{n+1}-y_{n} = thau * (b0 * f_{n+1} + b1 * f_{n} + b2 * f_{n-1} + b3 * f_{n-2} + ...)

        Args:
            k (int): Step 
            ret_str (bool, optional): Return string. Defaults to False.

        Return:
            list: K step Adams explicit method coefficients
        """
        matrix_to_get_coeffs = [[1] * k]
        extend_matrix = [[0] * k for _ in range(k-1)]
        matrix_to_get_coeffs.extend(extend_matrix)
        left_ = [1/m for m in range(1, k+1)]
        m = 1
        for k in range(1,len(matrix_to_get_coeffs)):
            row = matrix_to_get_coeffs[k]
            for j in range(1, len(row) + 1):
                row[j-1] =  j**m
            m += 1
        B = LinEqSolver.gauss_elimination(matrix_to_get_coeffs, left_, 15)
        if ret_str:
            return_str = ''
            for l in range(1, k + 1):
                return_str += f'+({B[l-1]}) * f_(n + ({1-l}))'
            return_str = "(Y_{n+1} - Y{n}) = thau * (" + return_str + ")"
            return B, return_str
        return B
                


    