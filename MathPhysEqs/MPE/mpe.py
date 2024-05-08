import sys, os
paths = [ 
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Lineq')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Nonlineq'))
]
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

import copy
from LinEq import LinEqSolver # import Lineq solver
from NonLinEq import Polynom, NonLinEqSolver

class MPE():
    """
    Class for solving MPE
    dy/dx = f(x, y) 
    y(x0) = y0

    f must be function of x,y
    Example:
    -------
    def f(x,y):
        return -x+y
    
    - `eiler(self, n)`: Eiler method
    - `heun(self, n`): Heun method
    - `k_step_Adams_explicit(self, k)`: K step Adams explicit method
    - `rk4(self, n)`: Runge-Kutta 4 method
    - `rk2(self, n)`: Runge-Kutta 2 method
    - `solve_Adams_KSE(self, k, n, preliminary_k_method)`: Solve using K step Adams explicit method


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
        n += 1
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
        n += 1
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
    

    def rk4(self, n):
        """
        RK4 - Runge-Kutta 4 method
            

        Args:
            n (int): Number of steps

        Return:
                list: Solution
        """
        theta = (self.Area[1] - self.Area[0])/n
        n += 1
        self.x = [self.Area[0]+theta*i for i in range(n)]
        result = [self.f0]
        x = self.Area[0]
        y = self.f0
        for i in range(1, n):
            k1 = theta * self.f(x, y)
            k2 = theta * self.f(x + theta/2, y + k1/2)
            k3 = theta * self.f(x + theta/2, y + k2/2)
            k4 = theta * self.f(x + theta, y + k3)
            y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
            x = x + theta
            result.append(y)
        
        return result
    


        

    def rk2(self, n):
        """
        RK2 - Runge-Kutta 2 method
            

        Args:
            n (int): Number of steps

        Return:
                list: Solution
        """
        theta = (self.Area[1] - self.Area[0])/n
        n += 1
        self.x = [self.Area[0]+theta*i for i in range(n)]
        result = [self.f0]
        x = self.Area[0]
        y = self.f0
        for i in range(1, n):
            k1 = theta * self.f(x, y)
            k2 = theta * self.f(x + theta, y + k1)
            y = y + (k1 + k2) / 2
            x = x + theta
            result.append(y)
        
        return result




    def solve_Adams_KSE(self, k, n, preliminary_k_method = "euler"):
        """
            Solve using K step Adams explicit method

        Args:
            k (int): Step
            n (int): Number of steps
            preliminary_k_method (str, optional): method to calculate first k steps. Defaults to "euler".
        
        Raise:
            ValueError: if k > (b-a)/h
        
        Notes:
            - if k > (b-a)/h, raise ValueError

        Example:
        -------
        >>> mpe = MPE((0, 1), lambda x, y: -x+y, 1)
        >>> mpe.solve_using_K_step_Adams_explicit(3, 4, "euler")
        
        Return:
            list: Solution
        """
        B = MPE.k_step_Adams_explicit(k)
        if preliminary_k_method not in ["euler", "heun", "rk4", "rk2", "gira2"]:
            raise ValueError('preliminary_k_method must be in ["euler", "heun", "rk4", "rk2", "gira2"]')
        
        theta = (self.Area[1] - self.Area[0])/n
        n += 1
        self.x = [self.Area[0]+theta*i for i in range(n)]

        if k > (self.Area[1] - self.Area[0]) / theta:
            raise ValueError('k > (b-a)/h')
        copy_ = MPE((self.Area[0], self.Area[0] + theta * k), self.f, self.f0)

        if preliminary_k_method == "euler":
            result = copy_.eiler(k)
        elif preliminary_k_method == "heun":
            result = copy_.heun(k)
        elif preliminary_k_method == "rk4":
            result = copy_.rk4(k)
        elif preliminary_k_method == "rk2":
            result = copy_.rk2(k)
        
        result = result[1:]
        for i in range(k, n-1):
            sum_ = theta * sum(B[l-1] * self.f(self.x[i-l], result[i-l]) for l in range(1, k+1))
            result.append(result[i-1] + sum_)
                
        result = [self.f0] + result
            
        return result
            

    