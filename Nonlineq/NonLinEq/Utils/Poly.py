import re
import warnings
import matplotlib.pyplot as plt
class Polynom:
    """
    A class for representing polynomials

    - `__init__(self, Poly)`: Initialize the polynomials
    - `__str__(self)`: Return a string representation of the Degree and Polynomial attributes with special character replacements.
    - `__eq__(self, other)`: Check if two polynomials are equal.
    - `__neq__(self, other)`: Check if two polynomials are not equal.
    - `__add__(self, other)`: Add two polynomials.
    - `__sub__(self, other)`: Subtract two polynomials.
    - `__mul__(self, other)`: Multiply two polynomials.
    - `__rmul__(self, other)`: Multiply a polynomial by a constant.
    - `__neg__(self)`: Negate the polynomial.
    - `__call__(self, value)`: Evaluate the polynomial expression with the given value for the variable.
    - `copy(self)`: Create a copy of the polynomial.
    - `polynomial_degree(poly_str)`: A method to calculate the degree of a polynomial expression.
    - `eval(self, value)`: Evaluate the polynomial expression with the given value for the variable.
    - `get_degree(self)`: A method to retrieve the degree attribute from the object.
    - `get_variable(self)`: Get the value of the Variable attribute.
    - `get_coeffs(self)`: Get the coefficients of the polynomial.
    - `get_diff(self)`: Get the derivative of the polynomial.
    - `plot(self, range, step)`: Plot the polynomial.


    """

    def __init__[T: list[list, str] | list[str, str] | 'Polynom'](self, Poly: T):
        """
        Initialize the polynomials

        Args:
            Poly (list[list, str], list[str, str]): A list containing the coefficients and the variable of the polynomial

        Raises:
            TypeError: If the input is not a list
            TypeError: If the elements in the list are not int or float
            ValueError: If the length of the list is not 2
        
        Notes:
                - The list should be of length 2
                - The first element of the list should be a list or string
                - The second element of the list should be a string

        Example:
        -------
        >>> Poly = [[1,2,3,4], 'x']
        >>> P = Polynom(Poly)

        >>> P
        'x**3 + 2*x**2 + 3*x + 4'
        """

        if type(Poly) == list:
            if len(Poly) != 2:
                raise ValueError("Poly should be a list of length 2")
            
            if type(Poly[1]) != str:
                warnings.warn("Poly[1] is not str\nPoly[1] will be set as 'x'")
                Poly[1] = 'x'
                
            if len(Poly[1]) != 1:
                warnings.warn("Poly[1] is not a single character\nPoly[1] will be set as 'x'")
                Poly[1] = 'x'

            self.Variable = Poly[1]
            self.Poly = ''
            if type(Poly[0]) == list:
                if not all(isinstance(elem, (int, float)) for elem in Poly[0]):
                    raise TypeError("Poly[0] is list\nAll elements in Poly[0] should be int or float")
                for i in Poly[0]:
                    if len(Poly[0])-Poly[0].index(i)-1 == 0:
                        if i >= 0:
                            self.Poly += f'+{i}'
                        if i < 0:
                            self.Poly += f'{i}'
                    elif i >= 0:
                        self.Poly += f'+{i}*'+str(self.Variable)+f'**{len(Poly[0])-Poly[0].index(i)-1}'
                    elif i < 0:
                        self.Poly += f'{i}*'+str(self.Variable)+f'**{len(Poly[0])-Poly[0].index(i)-1}'

                self.Degree = len(Poly[0])-1

            if type(Poly[0]) == str:
                
                self.Poly = Poly[0]
                self.Degree = Polynom.polynomial_degree(self.Poly)
        
        elif type(Poly) == Polynom:
            self.Poly = Poly.Poly
            self.Degree = Poly.Degree

        else:
            raise TypeError("Poly is not list")

    def __call__(self, value):
        """
        Evaluate the polynomial expression with the given value for the variable.
        """
        return self.eval(value)
    
    def __str__(self):
        """
        Return a string representation of the Degree and Polynomial attributes with special character replacements.
        """
        return f'Degree: {self.Degree}' + '\nPolynomial: ' + self.Poly.replace('**', '^').replace('-',' - ').replace('+',' + ').replace('*','')
    
    def __eq__(self, other):
        """
        Check if two polynomials are equal.
        """
        return self.get_coeffs() == other.get_coeffs() and self.Variable == other.Variable
    
    def __neq__(self, other):
        """
        Check if two polynomials are not equal.
        """
        return not self == other

    def __mul__(self, other):
        """
        Multiply two polynomials.
        """
        if isinstance(other, Polynom):
            if self.Variable != other.Variable:
                raise ValueError('Polynomials must have the same variable')
            _s = self.get_coeffs()
            _v = other.get_coeffs()
            res = [0]*(len(_s)+len(_v)-1)
            for selfpow,selfco in enumerate(_s):
                for valpow,valco in enumerate(_v):
                    res[selfpow+valpow] += selfco*valco
        else:
            res = [coef * other for coef in self.get_coeffs()]
        return Polynom([res, self.Variable])
    
    def __rmul__(self, other):
        return self * other
    
    def __add__(self, other):
        """
        Add two polynomials together.
        """
        if type(other) != Polynom:
            other = Polynom(other)
        if self.Variable != other.Variable:
            raise ValueError('Polynomials must have the same variable')
        
        self_coef = self.get_coeffs()
        other_coef = other.get_coeffs()
        new_coefs = []
        sb = abs(len(self_coef) - len(other_coef))
        if len(self_coef) == len(other_coef):
            for i in range(len(self_coef)):
                new_coefs.append(self_coef[i] + other_coef[i])
                
        if len(self_coef) > len(other_coef):
            
            for i in range(len(self_coef)):
                if len(self_coef) - len(other_coef) - i > 0:
                    new_coefs.append(self_coef[i])
                else:
                    new_coefs.append(self_coef[i] + other_coef[i-sb])

        elif len(self_coef) < len(other_coef):
            return other + self
        
        return Polynom([new_coefs, self.Variable])
    
    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other
    
    def __sub__(self, other):
        """
        Subtract two polynomials.
        """
        return self + -other

    def __neg__(self):
        """
        Negate the polynomial.
        """
        self_coef = self.get_coeffs()
        coefs = [-coef for coef in self_coef]
        variable = self.Variable
        return Polynom([coefs, variable])

    def copy(self):
        """
        Create a copy of the polynomial.
        """
        return Polynom([self.get_coeffs(), self.Variable])
    

    def get_coeffs(self):
        """
        Get the coefficients of the polynomial.
        """
        coefficients = [float(coef) for coef in re.findall(r'[-+]?\d*\.?\d+', self.Poly)]
        coefficients = coefficients[::2]
        return coefficients


    def eval(self, value):
        """
        Evaluate the polynomial expression with the given value for the variable.

        Parameters:
            value (numeric): The value to substitute for the variable in the polynomial expression.

        Returns:
            numeric: The result of evaluating the polynomial expression with the given value.
        """
        return eval(self.Poly, {self.Variable: value})

    def get_degree(self):
        """
        A method to retrieve the degree attribute from the object.
        """
        return self.Degree
    
    def get_variable(self):
        """
        Get the value of the Variable attribute.
        """
        return self.Variable

    def polynomial_degree(poly_str):
        """
        A method to calculate the degree of a polynomial expression.

        Parameters:
            poly_str (str): The string representation of the polynomial expression.

        Returns:
            int: The degree of the polynomial expression.
        """
        exponents = re.findall(r'\*{2}(\d+)', poly_str)
        
        if exponents:
            degrees = [int(exp) for exp in exponents]
            return max(degrees)
        else:
            return 0  
        
    def get_diff(self):
        """
        Get the derivative of the polynomial.
        """
        coeffs = self.get_coeffs()
        new_coeffs = []
        for i in range(0, len(coeffs)-1):
            new_coeffs.append(coeffs[i] * (len(coeffs)-i-1))    

        return Polynom([new_coeffs, self.Variable])


    def plot(self, range: tuple = (-10, 10), step: float = 0.1, colors = ['blue'], **kwargs):
        """
        Plot the polynomial.

        Parameters:
            variable (str): The variable to plot the polynomial on.
            range (list): The range of the x-axis.
            step (float): The step size for the x-axis.
            kwargs: 
                Additional arguments to pass to the plot function.
                list of tuples or list of lists: [(x1, y1), (x2, y2), ...]
                for plotting 
        
        Raises:
            ValueError: If the length of the lists/typles in args is not 2
            ValueError: If the args is not a list
            ValueError: If the elements in the args elements are not int or float

        Returns:
            None
        """

        if len(colors) == 0:
            warnings.warn('No colors provided, using default color blue')
            colors = ['blue']

        if type(colors[0]) != str:
            raise ValueError('The first color must be a string')

        if type(colors[1]) != str:
            raise ValueError('The second color must be a string')
        
        x, y = [], []
        point = range[0]
        while point < range[1]:
            x.append(point)
            y.append(self(point))
            point += step

        if kwargs:
            points = dict()
            for key, arg in kwargs.items():
                points[key] = [[],[]]
                if type(arg) == list or type(arg) == tuple:
                    for pts in arg:
                        if len(pts) == 2:
                            if isinstance(pts[0], int) or isinstance(pts[1], float):
                                points[key][0].append(pts[0])
                                points[key][1].append(pts[1])
                            else:
                                raise ValueError(f'Invalid argument {pts} in {arg} in {kwargs}')
                        else:
                            raise ValueError(f'Invalid argument {pts} in {arg} in {kwargs}')
                else:
                    raise ValueError(f'Invalid argument {arg} in {kwargs}')

        plt.title(str(self))
        plt.xlabel(self.Variable)
        plt.ylabel(f'P({self.Variable})')

        plt.grid(True)
        plt.plot(x, y, color = colors[0], label = f'P({self.Variable})') 
        
        if kwargs:
            i = 0
            for key, item  in points.items():
                try:
                    color = colors[i+1]
                except:
                    color = colors[-1]
                plt.scatter(item[0], item[1], color = color, label = key)
                i+=1
        
        plt.legend()
        plt.show()
