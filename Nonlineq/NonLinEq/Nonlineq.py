import warnings
import sys
import os
import importlib


from .Utils.Poly import Polynom as Poly

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Lineq'))
if path not in sys.path:
    sys.path.append(path)

from LinEq import LinEqSolver # import Lineq solver



class NonLinEqSolver:
    """
    A class for solving non-linear equations

    - `solve(self, eps, mode, step)`: Solve the non-linear equation
    - `bisect_solver(self, eps, step)`: Bisection method for solving the equation P(n) = 0
    - `find_intervals_with_opposite_signs(self, start, end, step)`: Find the intervals with opposite signs in the domain
    - `newton_solver(self, eps, step)`: Newton method for solving the equation P(n) = 0
    - `iter_sim_solver(self, eps, step, max_iter)`: Iterative SIM method for solving the equation P(n) = 0

    Example
    -------
    >>> from NonLinEq import Polynom, NonLinEqSolver
    >>> a = Polynom([[-1,0,9],'x'])
    >>> b = NonLinEqSolver(Polynom = a, Area = (-3,3))
    >>> print(b.solve(mode = 'bisect', eps = 1e-6, step = 0.1))

    """

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        kwargs
            Polynom: Polynomial to be solved 
            Area: Area of the domain of the equation
        """
        if kwargs['Polynom'] is None:
            raise ValueError('Polynomial cannot be None')
        
        if type(kwargs['Polynom']) is not Poly:
            self.Polynom = Poly(kwargs['Polynom'])
        else:
            self.Polynom = kwargs['Polynom']

        self.domain = kwargs['Area']

    def __str__(self):
        return str(self.Polynom)

    
    def solve(self, eps: float = 1e-6, mode: str = 'bisect', step = 0.1, **kwargs):
        """
        Solve the non-linear equation

        Args:
            - mode (str): The method to use for solving the non-linear equation. Defaults to 'bisect'.
                - `The method list`
                    - bisect
                    - iter_sim
                    - newton
            
            eps (float): The tolerance for the bisection method. Defaults to 1e-6.
            step (float): The step size for the intervals search. Defaults to 0.1.
            - kwargs:
                - max_iter (int): The maximum number of iterations. Defaults to 100.
        Returns:
            list: A list of solutions to the equation P(n) = 0

        """
        try:
            max_iter = kwargs['max_iter']
        except:
            max_iter = 100
            warnings.warn("max_iter not specified, using default value of 100")
        
        if mode == 'bisect':
            return self.bisect_solver(eps=eps, step=step)

        elif mode == 'iter_sim':
            return self.iter_sim_solver(eps=eps, step=step, max_iter=max_iter)

        elif mode == 'newton':
            return self.newton_solver(eps=eps, step=step)


    def find_intervals_with_opposite_signs(self, start, end, step=0.1):
        """
        Find the intervals with opposite signs in the domain
        
        Args:
            start (float): The starting value of the domain
            end (float): The ending value of the domain
            step (float): The step size. Defaults to 0.1.

        Raises:
            ValueError: If the step size is not positive

        Returns:
            intervals (list): A list of intervals with opposite signs
        """
        if step < 0:
            raise ValueError('Step size must be positive')
        
        Poly = self.Polynom
        intervals = []
        x = start-1e-15
        
        while x < end:
            x_next = x + step
            if Poly.eval(x) * Poly.eval(x_next) < 0:
                intervals.append((x, x_next))
            x = x_next
        return intervals

    def iter_sim_solver(self, eps: float = 1e-6, step = 0.1, max_iter = 100):
        """
        Solve the nonlinear equation using iterative simulation.
        
        Args:
            eps (float, optional): The desired accuracy of the solution. Defaults to 1e-6.
            step (float, optional): The step size for interval subdivision. Defaults to 0.1.
            max_iter (int, optional): The maximum number of iterations for the algorithm. Defaults to 100.
        
        Raises:
            ValueError: If the desired accuracy is not a positive number.
            ValueError: If the step size is not a positive number.
            ValueError: If the maximum number of iterations is not a positive integer.
        
        Returns:
            list: A list of solutions found in the given domain.
        """
        a = self.domain[0]
        b = self.domain[1]
        solutions = []
        subintervals = self.find_intervals_with_opposite_signs(a, b, step)
        degree = self.Polynom.get_degree()-1
        member = f'{self.Polynom.get_variable()}**{degree}'
        coefs = self.Polynom.get_coeffs()
        coefs.pop(0)
        new_Poly = -1*Poly([coefs, self.Polynom.get_variable()])
        if subintervals != []:
            for interval in subintervals:
                start_value = (interval[0] + interval[1])/2
                for _ in range(max_iter):
                    new_value = (new_Poly).eval(start_value)/eval(member, {self.Polynom.get_variable(): start_value})
                    if abs(start_value - new_value) < eps:
                        if new_value > interval[0] and new_value < interval[1]:
                            solutions.append(new_value)
                        break
                    start_value = new_value
        
        else:
            raise ValueError(f'No intervals with opposite signs found in [{a}, {b}] with step = {step}\n please decrease the step size')
        
        if solutions != []:
            return solutions
        
        else:
            warnings.warn(f'No solution found in [{self.domain[0]}, {self.domain[1]}]')



    def newton_solver(self, eps: float = 1e-6, step = 0.1, max_iter = 100):
        """
        Solve the nonlinear equation using Newton's method.
        
        Args:
            eps (float, optional): The desired accuracy of the solution. Defaults to 1e-6.
            step (float, optional): The step size for interval subdivision. Defaults to 0.1.
            max_iter (int, optional): The maximum number of iterations for the algorithm. Defaults to 100.
        
        Raises:
            ValueError: if no intervals with opposite signs found in the domain
            
        Returns:
            list: A list of solutions found in the given domain.
        """

        a = self.domain[0]
        b = self.domain[1]
        solutions = []
        subintervals = self.find_intervals_with_opposite_signs(a, b, step)
        if subintervals != []:
            for interval in subintervals:
                start_value = (interval[0] + interval[1])/2
                for _ in range(max_iter):
                    new_value = start_value - self.Polynom.eval(start_value)/self.Polynom.get_diff().eval(start_value)
                    if abs(start_value - new_value) < eps:
                        if new_value > interval[0] and new_value < interval[1]:
                            solutions.append(new_value)
                        break
                    start_value = new_value
        
        else:
            raise ValueError(f'No intervals with opposite signs found in [{a}, {b}] with step = {step}\n please decrease the step size')
        
        if solutions != []:
            return solutions
        
        else:
            warnings.warn(f'No solution found in [{self.domain[0]}, {self.domain[1]}]')

    def bisect_solver(self, eps: float = 1e-6, step = 0.1):
        """
        Bisection method for solving the equation P(n) = 0

        Args:
            eps (float): The tolerance for the bisection method. Defaults to 1e-6.
            step (float): The step size for the bisection method. Defaults to 0.1.

        Raises:
            ValueError: If there are no intervals with opposite signs

        Notes:
            The bisection method is used to find the solution to the equation P(n) = 0

        Returns:
            list: A list of solutions to the equation P(n) = 0

        """
        a = self.domain[0]
        b = self.domain[1]
        solutions = []
        subintervals = self.find_intervals_with_opposite_signs(a, b, step)

        if subintervals != []:
            for interval in subintervals:
                a = interval[0]
                b = interval[1]              
                fa = self.Polynom.eval(a) 
                
                while abs(b-a) > eps:
                    c = (a+b)/2
                    fc = self.Polynom.eval(c)
                    if fc*fa < 0:
                        b = c
                    else:
                        a = c
                solutions.append(c)
        else:
            raise ValueError(f'No intervals with opposite signs found in [{a}, {b}] with step = {step}\n please decrease the step size')
        
        if solutions == []:
            warnings.warn(f'No solution found in [{self.domain[0]}, {self.domain[1]}]')
        return solutions
         
    
