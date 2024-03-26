import re
import warnings
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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
    - `plot(self, range, step, colors, legend, **kwargs)`: Plot the polynomial.


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
                
            if len(Poly[1]) > 1 and Poly[1][0] != '(' and Poly[1][-1] != ')':
                    Poly[1] = "("+Poly[1]+')'

            count = 0
            for i in Poly[1]:
                if i == '(':
                    count += 1
                if i == ')':
                    count -= 1
            if count != 0:
                raise ValueError("There is not matching closing/opening bracket for an opening/closing bracket")
            
            if Poly[1][-1] != ')' and len(Poly[1]) != 1:
                Poly[1] = "("+Poly[1]+')'              

            self.Variable = Poly[1]
            self.Poly = ''
            if type(Poly[0]) == list:
                if not all(isinstance(elem, (int, float)) for elem in Poly[0]):
                    raise TypeError("Poly[0] is list\nAll elements in Poly[0] should be int or float")
                for i in Poly[0][0:-1]:
                    if i >= 0:
                        self.Poly += f'+{i}*'+str(self.Variable)+f'**{len(Poly[0])-Poly[0].index(i)-1}'
                    elif i < 0:
                        self.Poly += f'{i}*'+str(self.Variable)+f'**{len(Poly[0])-Poly[0].index(i)-1}'
                
                if Poly[0][-1] >= 0:
                        self.Poly += f'+{Poly[0][-1]}'
                if Poly[0][-1] < 0:
                        self.Poly += f'{Poly[0][-1]}'

                self.Degree = len(Poly[0])-1

            if type(Poly[0]) == str:
                
                self.Poly = Poly[0]
                self.Degree = Polynom.polynomial_degree(self.Poly)
        
        elif type(Poly) == Polynom:
            self.Poly = Poly.Poly
            self.Degree = Poly.Degree

        else:
            raise TypeError("Poly is not list")

        variable = ''
        for letter in Poly[1]:
            if letter.isalpha():
                variable += letter

        self.Variable = variable if variable else 'x'
        if len(Poly[1]) == 1:
            self.Variable = Poly[1]

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
        if isinstance(other, (int, float)):
            other = Polynom([[other], self.Variable])

        if type(other) != Polynom and isinstance(other, (int, float)):
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
        coefficients = [float(coef) for coef in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', self.Poly)]
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


    def plot(self, range: tuple = (-10, 10), step: float = 0.1, colors = ['blue'], legend = True, **kwargs):
        """
        Plot the polynomial.

        Parameters:
            variable (str): The variable to plot the polynomial on.
            range (list): The range of the x-axis.
            step (float): The step size for the x-axis.
            colors (list): The colors to use for the plot first color uses to self, others to additional points.
            legend (bool): Whether to show the legend.
            for poly-s and func-s use syntax of kwargs['func'] kwargs['poly']
            - kwargs: 
                - Additional arguments to pass to the plot function.
                list of tuples or lists (elements must be int or float and must have length 2) : [(x1, y1), (x2, y2), ...] ot [[x1, y1], [x2, y2], ...] or [(x1, y1], (x2, y2), ...])] points to plot
                

                - func: 
                    - the functions to plot 
                    - can be list of functions or a single function.
                    - if single function for color and name may be provided as a tuple (func, color, name)
                    - if color is not provided will be 'blue'
                    - if name is not provided will be the 'func'
                    - Examples: 
                        - func = [(func1, color, name), [func2, color], func3 ...]
                        - func = (func1, color, name)
                        - func = func1
                    
                - poly:
                    - the additional polynomials to plot 
                    - can be list of polynomials or a single polynomial.
                    - if single polynomial for color and name may be provided as a tuple (poly, color, name) [same as func]
                    - if color is not provided will be 'blue'
                    - if name is not provided will be the Polynom Str representation slice [23:end]
                        -   Example:
                            - poly3 = Polynom('x**3 + 2*x**2 + 3*x + 4')
                            - poly = poly.plot(range = (-3,3), step=0.01, colors=['blue', 'green'], poly = poly3)   
                            - Poly3.name # in legend
                            - x^3 + 2x^2 + 3x + 4
                            - Poly3.color # in plot and legend
                            - 'black'

                    - Examples: 
                        - poly = [(poly1, color, name), [poly2, color], poly3 ...]
                        - poly = (poly1, color, name)
                        - poly = poly1
                            

        Example:
        -------
        >>> def funct(x):
        >>>     return cos(x)*sin(x*pi)+sqrt(5+x)

        >>> a = Polynom([[1, 3, 0, -1.0],'(x-0.25)'])
        >>> b = Polynom([3,4,-1], 'x')
        >>> a.plot(range = (-3,3), step=0.01, colors=['blue', 'green'], solutions = plot, func = (funct, 'purple', 'cos(x)*sin(x*pi)+sqrt(5+x)')
        poly = b)
        >>> #in example plot is list of points [(x1,y1),(x2,y2), ...] of solution of P(x) = a = 0
           
        
        
        Raises:
            ValueError: If the length of the lists/typles in args is not 2
            ValueError: If the args is not a list
            ValueError: If the elements in the args elements are not int or float

        Returns:
            None
        """
        def check_color_existence(color_name):
            try:
                mcolors.to_rgba(color_name)
                return True
            except ValueError:
                return False


        if len(colors) == 0:
            warnings.warn('No colors provided, using default color blue')
            colors = ['blue']

        for color in colors:
            if not check_color_existence(color):
                raise ValueError(f'Invalid color {color}')
        
        x, y = [], []
        point = range[0]
        while point < range[1]+step:
            x.append(point)
            y.append(self(point))
            point += step

        if kwargs:
            points = dict()
            for key, arg in kwargs.items():
                if key != 'func' and key != 'poly':
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
        plt.plot(x, y, color = colors[0], label = f'P({self.Variable}) : {str(self)[23:]}') 
        if 'func' in kwargs.keys():
            if type(kwargs['func']) == list:
                for element in kwargs['func']:
                    if type(element) == tuple or type(element) == list:

                        color = element[1] if check_color_existence(element[1]) else 'black'
                        
                        try: 
                            name = element[2]
                        except:
                            name = f'func{kwargs["func"].index(element)}'

                        if type(element[0]) == type(lambda: None):
                            plt.plot(x, [element[0](i) for i in x], color = color, label =  name)

                    elif type(element) == type(lambda: None):
                        plt.plot(x, [element(i) for i in x], color = 'black', label = f'func{kwargs["func"].index(element)}')

            elif type(kwargs['func']) == tuple:
                
                color = kwargs['func'][1] if check_color_existence(kwargs['func'][1]) else 'black'

                try:
                    name = kwargs['func'][2]
                except:
                    name = 'func0'

                if type(kwargs['func'][0]) == type(lambda: None):
                    plt.plot(x, [kwargs['func'][0](i) for i in x], color = color, label = name)

            elif type(kwargs['func']) == type(lambda: None):
                plt.plot(x, [kwargs['func'](i) for i in x], color = 'black', label = 'func0')
            
        if 'poly' in kwargs.keys():
            if type(kwargs['poly']) == list:
                for element in kwargs['poly']:
                    if type(element) == tuple or type(element) == list:

                        color = element[1] if check_color_existence(element[1]) else 'black'

                        try:
                            name = element[2]

                        except:
                            name = f'P({element[0].Variable}) : {str(element[0])[23:]}'

                        if type(element[0]) == Polynom:
                            plt.plot(x, [element[0](i) for i in x], color = color, label = name)

                    elif type(element) == Polynom:
                        plt.plot(x, [element(i) for i in x], color = 'black', label = f'P({element.Variable}) : {str(element)[23:]}')

            elif type(kwargs['poly']) == tuple:

                color = kwargs['poly'][1] if check_color_existence(kwargs['poly'][1]) else 'black'
                
                try:
                    name = kwargs['poly'][2]

                except:
                    name = f'P({kwargs["poly"][0].Variable}) : {str(kwargs["poly"][0])[23:]}'

                if type(kwargs['poly'][0]) == Polynom:
                    plt.plot(x, [kwargs['poly'][0](i) for i in x], color = color, label = name)

            elif type(kwargs['poly']) == Polynom:
                plt.plot(x, [kwargs['poly'](i) for i in x], color = 'black', label = f'P({kwargs['poly'].Variable}) : {str(kwargs['poly'])[23:]}')
            
        if kwargs:
            i = 0
            for key, item  in points.items():
                try:
                    color = colors[i+1]
                except:
                    color = colors[-1]
                plt.scatter(item[0], item[1], color = color, label = key)
                i+=1
        if legend:
            plt.legend()
        plt.show()

