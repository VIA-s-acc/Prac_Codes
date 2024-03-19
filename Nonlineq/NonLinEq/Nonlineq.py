from .Utils.Poly import Polynom as Poly
import warnings

class NonLinEqSolver:
    """
    A class for solving non-linear equations

    - `solve(self, eps, mode, step)`: Solve the non-linear equation
    - `bisect_solver(self, eps, step)`: Bisection method for solving the equation P(n) = 0

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

    
    def solve(self, eps: float = 1e-6, mode: str = 'bisect', step = 0.1):
        """
        Solve the non-linear equation

        Args:
            - mode (str): The method to use for solving the non-linear equation. Defaults to 'bisect'.
                - `The method list`
                - bisect
                - iter_sim
                - newton
        
        Returns:
            list: A list of solutions to the equation P(n) = 0

        """


        if mode == 'bisect':
            return self.bisect_solver(eps=eps, step=step)

        elif mode == 'iter_sim':
            pass

        elif mode == 'newton':
            pass


    def find_intervals_with_opposite_signs(self, start, end, step=0.1):
        """
        Find the intervals with opposite signs in the domain
        
        Args:
            start (float): The starting value of the domain
            end (float): The ending value of the domain
            step (float): The step size. Defaults to 0.1.


        Returns:
            intervals (list): A list of intervals with opposite signs
        """
        Poly = self.Polynom
        intervals = []
        x = start-1e-15
        
        while x < end:
            x_next = x + step
            if Poly.eval(x) * Poly.eval(x_next) < 0:
                intervals.append((x, x_next))
            x = x_next
        return intervals


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
            raise ValueError(f'No intervals with opposite signs found in [{a}, {b}]')
        
        if solutions == []:
            warnings.warn(f'No solution found in [{a}, {b}]')
        return solutions
         
    
