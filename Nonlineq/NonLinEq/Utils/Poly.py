import re
import warnings
class Polynom:
    """
    A class for representing polynomials

    - `__init__(self, Poly)`: Initialize the polynomials
    - `__str__(self)`: Return a string representation of the Degree and Polynomial attributes with special character replacements.
    - `polynomial_degree(poly_str)`: A method to calculate the degree of a polynomial expression.
    - `eval(self, value)`: Evaluate the polynomial expression with the given value for the variable.
    - `get_degree(self)`: A method to retrieve the degree attribute from the object.
    - `get_variable(self)`: Get the value of the Variable attribute.

    """

    def __init__[T: list[list, str] | list[str, str] | 'Polynom'](self, Poly: T):
        

        if type(Poly) == list:
            
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
                        if i > 0:
                            self.Poly += f'+{i}'
                        if i < 0:
                            self.Poly += f'{i}'
                    elif i > 0:
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

    def __str__(self):
        """
        Return a string representation of the Degree and Polynomial attributes with special character replacements.
        """
        return f'Degree: {self.Degree}' + '\nPolynomial: ' + self.Poly.replace('**', '^').replace('-',' - ').replace('+',' + ').replace('*','')
    
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

