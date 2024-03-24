import re
import warnings
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

