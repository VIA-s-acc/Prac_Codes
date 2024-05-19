import sys, os
paths = [ 
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Lineq')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Nonlineq'))
]
for path in paths:
    if path not in sys.path:
        sys.path.append(path)
from warnings import warn
import copy
from LinEq import LinEqSolver # import Lineq solver
from NonLinEq import Polynom, NonLinEqSolver

class MPE():
    """
    Class for solving MPE
    dy/dx = f(x, y) \\
    y(x0) = y0

    f must be function of x,y
    Example:
    -------
    def f(x,y):
        return -x+y
    -------
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
        if preliminary_k_method not in ["euler", "heun", "rk4", "rk2"]:
            raise ValueError('preliminary_k_method must be in ["euler", "heun", "rk4", "rk2"]')
        
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
    
def finit_diff(f, a, b, n, d, m1, m2):
    """
    function to solve the equation \\
    d^2u/dx^2 + q(x)u(x) = f(x)\\
    u(a) = m1\\
    u(b) = m2\\
    q(x) >= q(a) >= 0

    Args:
        f (function): function
        a (float): lower bound
        b (float): upper bound
        n (int): number of subintervals
        d (function): derivative
        m1 (float): first parameter
        m2 (float): second parameter

    Raises:
        TypeError: if f or d is not a function
        ValueError: if a is greater than b or n is less than 1

    Notes:
        - if a is greater than b or n is less than 1, raise ValueError
        
    Return:
            list: Solution
    """
    if type(f) != type(lambda x: None):
        raise TypeError('f must be a function')
    if type(d) != type(lambda x: None):
        raise TypeError('d must be a function')
    if b > a:
        a, b = b, a
    if a == b or n == 0:
        raise ValueError('a must be different from b and n must be greater than 0')
    h = (b-a)/n
    x = [a + i*h for i in range(n+1)]
    A = [[0] * (n-1)] * (n-1)
    b = [0] * (n-1)
    for i in range(1, n):
        xi = a + i*h
        di = d(xi)
        fi = f(xi)
        if i == 1:
            A[i-1][i-1] = -2/h**2 + di
            A[i-1][i] = 1/h**2
            b[i-1] = fi - m1/h**2
        if i == n-1:
            A[i-1][i-2] = 1/h**2
            A[i-1][i-1] = -2/h**2 + di
            b[i-1] = fi - m2/h**2
        else:
            A[i-1][i-2] = 1/h**2
            A[i-1][i-1] = -2/h**2 + di
            A[i-1][i] = 1/h**2
            b[i-1] = fi
    y = LinEqSolver.tridiagonal_elimination(A, b, 15)
    y = [m1] + y + [m2]
    return y, x #????

class BVP:
    """
    class for boundary value problem solving for the equation of thermal conduction
    du/dt = alpha * d^2u/dx^2 + f(t, x) \\
    u(t, a) = m1  \\
    u(t, b) = m2 \\
    u(0, x) = v0(x) \\
    0 < x < L \\
    0 < t < T 
    - `__init__(self, T, L, m1, m2, v0, f)` : Initialize the boundary value problem solver for the equation of thermal conduction.
    - `solve_heat_equation(self, N, M, scheme, omega)` : Solve the boundary value problem for the equation of thermal conduction.
    - `_solve_heat_equation_explicit(self, N, M)` : Solve the boundary value problem for the equation of thermal conduction. (explicit scheme)
    - `_solve_heat_equation_implicit(self, N, M)` : Solve the boundary value problem for the equation of thermal conduction. (implicit scheme)
    - `_solve_heat_equation_weighted(self, N, M, omega)` : Solve the boundary value problem for the equation of thermal conduction. (weighted scheme)
    """
    def __init__(self, T, L, m1, m2, v0, f, alpha = 1):
        """
        Initialize the boundary value problem solver for the equation of thermal conduction.

        Args:
            T: Total time period
            L: Length of the domain
            m1: Boundary value at the left boundary
            m2: Boundary value at the right boundary
            v0: Initial condition function
            f: Function representing the right side of the equation f(x,t)
            alpha: Diffusion coefficient
        
        Returns:
            None
        """

        self.T = T
        self.L = L
        self.m1 = m1
        self.m2 = m2
        self.v0 = v0
        self.f = f
        self.alpha = alpha
        
    
    def _solve_heat_equation_explicit(self, N, M):
        """
        Solve the boundary value problem for the equation of thermal conduction. (explicit scheme)

        Args:
            N: Number of time steps
            M: Number of space steps

        Returns:
            list: Solution to the boundary value problem
        """
        delta_t = self.T / N
        delta_x = self.L / M
        if not delta_t <= delta_x**2/(2*self.alpha**2):
            warn("The time step is too large. The solution may not be accurate.", RuntimeWarning)
            warn("Stability condition: delta_t <= delta_x**2/(2*alpha**2)", RuntimeWarning)
        u = [[0.0 for _ in range(M+1)] for _ in range(N)]
        
        for k in range(M+1):
            u[0][k] = self.v0(k * delta_x) #нулевой ярус заполнен

        for n in range(1, N):
            
            u[n][0] = self.m1(n * delta_t)
            u[n][M] = self.m2(n * delta_t)
            
        const = self.alpha * delta_t / delta_x**2
        for n in range(0, N-1):
            for k in range(1, M):
                u[n + 1][k] = (
                    u[n][k] 
                    + const * (u[n][k - 1] - 2 * u[n][k] + u[n][k + 1]) 
                    + delta_t * self.f(k*delta_x, n*delta_t)
                )

        return u
    
    def _solve_heat_equation_implicit(self, N, M):
        """
        Solve the boundary value problem for the equation of thermal conduction. (implicit scheme)

        Args:
            N: Number of time steps
            M: Number of space steps

        Returns:
            list: Solution to the boundary value problem
        """
        delta_t = self.T / N
        delta_x = self.L / M

        u = [[0.0 for _ in range(M+1)] for _ in range(N)]
        const = self.alpha * delta_t / delta_x**2
        for k in range(M+1):
            u[0][k] = self.v0(k * delta_x) #нулевой ярус заполнен

        for k in range(1, N):
            u[k][0] = self.m1(k * delta_t)
            u[k][-1] = self.m2(k * delta_t)

        A = [[-const if j == i-1 else 1+2*const if j == i else -const if j == i+1 else 0 for j in range(M+1)] for i in range(M+1)]

        for k in range(0, N-1):
            
            B = [0.0 for _ in range(M+1)]
            B[0] = u[k][0]
            B[-1] = u[k][-1]
            for i in range(1, M):
                B[i] = delta_t * self.f(i*delta_x, k*delta_t) + u[k][i]

            
            u_row = LinEqSolver.tridiagonal_elimination(A, B, 15)
            for i in range(1, M):
                u[k+1][i] = u_row[i]

        
        return u
    
    def _solve_heat_equation_weighted(self, N, M, omega = 0.5):
        """
        Solve the boundary value problem for the equation of thermal conduction. (weighted scheme)

        Args:
            N: Number of time steps
            M: Number of space steps
            omega: Weight

        Returns:
            list: Solution to the boundary value problem
        """
        delta_t = self.T / N
        delta_x = self.L / M

        u = [[0.0 for _ in range(M+1)] for _ in range(N)]
        const = self.alpha * delta_t / delta_x**2
        for k in range(M+1):
            u[0][k] = self.v0(k * delta_x) #нулевой ярус заполнен

        for k in range(1, N):
            u[k][0] = self.m1(k * delta_t)
            u[k][-1] = self.m2(k * delta_t)

        A = [[-const*omega if j == i-1 else 1+2*const*omega if j == i else -const*omega if j == i+1 else 0 for j in range(M+1)] for i in range(M+1)]

        for k in range(0, N-1):
            B = [0.0 for _ in range(M+1)]
            B[0] = u[k][0]
            B[-1] = u[k][-1]
            for i in range(1, M):
                B[i] = delta_t * self.f(i*delta_x, k*delta_t) + u[k][i] + ( 1 - omega) * const * (u[k][i-1] - 2 * u[k][i] + u[k][i+1])
            u_row = LinEqSolver.tridiagonal_elimination(A, B, 15)
            for i in range(1, M):
                u[k+1][i] = omega * u_row[i] 


        return u



    def solve_heat_equation(self, N, M, scheme = "explicit", omega = 0.5):
        """
        Solve the boundary value problem for the equation of thermal conduction. (explicit scheme)

        Args:
            N: Number of time steps
            M: Number of space steps
            scheme: scheme list: ["explicit", "implicit", "weighted"]
            omega: Weight for weighted scheme

        Returns:
            list: Solution to the boundary value problem
        """
        if scheme not in ["explicit", "implicit", "weighted"]:
            warn("Invalid scheme. Choose from 'explicit', 'implicit', 'weighted'.", SyntaxWarning)
            warn("Using 'explicit' scheme.", SyntaxWarning)
            scheme = "explicit"
        if scheme == "explicit":
            return self._solve_heat_equation_explicit(N, M)
        elif scheme == "implicit":
            return self._solve_heat_equation_implicit(N, M)
        elif scheme == "weighted":
            return self._solve_heat_equation_weighted(N, M, omega)

    
    
        


    