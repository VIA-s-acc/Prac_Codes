
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

    