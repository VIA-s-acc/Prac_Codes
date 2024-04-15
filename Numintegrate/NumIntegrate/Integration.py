


class Integrate():
    """
    Class for numerical integration

    - `squares(mode)`: Calculate the integral using the sum of squares
    - `Simpson()`: Calculate the integral using Simpson method
    - `Trapeze()`: Calculate the  integrals using trapeze method
    
    """

    def __init__(self, func = None, interv: tuple = (0, 1), n: int = 100):
        """
        Integrate function
        
        Args:
            func (function): function to integrate
            a (float): lower bound
            b (float): upper bound
            n (int): number of subintervals

        Returns:
            float: result of integration
        """
        if type(func) == type(lambda x: None):
            self.func = func
        if interv[0] > interv[1]:
            interv = interv[::-1]
        self.a = interv[0]
        self.b = interv[1]
        self.n = n
        self.h = (self.b - self.a) / n
        self.x = [self.a + i * self.h for i in range(n + 1)]

    def squares(self, mode: str = 'right'):
        """
        Calculate the integral using the sum of squares

        Args:
            mode (str, optional): used formule to calculate the sum of squares. 'right', 'left' or 'center'. Defaults to 'right'.

        Returns:
            float: result of integration
        """
        sum = 0
        if mode == 'right':
            for i in range(0, self.n - 1):
                sum += self.func(self.x[i])*self.h
            return sum
        elif mode == 'left':
            for i in range(1, self.n):
                sum += self.func(self.x[i])*self.h
            return sum
        elif mode == 'center':
            for i in range(1, self.n - 1):
                sum += self.func((self.x[i-1] + self.x[i])/2)*self.h
            return sum
        else:
            raise ValueError("mode must be 'right', 'left' or 'center'")
    
    def Trapeze(self):
        """
        Calculate the  integrals using trapeze method

        Returns:
            float: result of integration
        """
        sum = 0
        for i in range(0, self.n):
            sum += self.h*(self.func(self.x[i]) + self.func(self.x[i-1]))/2
        return sum
    
    def Simpson(self):
        """
        Calculate the integral using Simpson method

        Returns:
            float: result of integration
        
        """
        if self.n % 2 != 0:
            raise ValueError("n must be even")
        sum = self.h/3 * (self.func(self.x[0]) + self.func(self.x[-1]))
        for i in range(1, self.n//2):
                sum += 2*self.func(self.x[2*i])*self.h/3
        for i in range(1, self.n//2+1):
                sum += 4*self.func(self.x[2*i-1])*self.h/3
        return sum
        
        
