import matplotlib.pyplot as plt
import numpy as np
class Plotter():
    """
        Class for plotting MPE
        - `plot(self, **kwargs)`: Plot functions or points
    """

    def __init__(self, Area):
        self.Area = Area

    def plot(self, **kwargs):
        """
            Plot functions or points
        Args:
            **kwargs:
                step (float, optional): Step. Defaults to 0.1.
                func* (list, optional): List of functions. Defaults to [].
                pts* (list, optional): List of points. Defaults to [].
                legend (bool, optional): Legend. Defaults to True.
                func* means func1, func2, func3, ... or something else
                pts* means pts1, pts2, pts3, ... or something else
        """ 
        if 'legend' in kwargs.keys():
            legend = kwargs['legend']
            if type(legend) != type(False):
                legend = False
                print("legend must be bool")
                print("set legend = False")
        else:
            legend = True
        if 'step' in kwargs.keys():
            step = kwargs['step']
        else:
            step = 0.1
        func = []
        pts = []
        for i in kwargs.keys():
            if i.startswith('func'):
                func.append(kwargs[i])
            if i.startswith('pts'):
                pts.append([kwargs[i], i])
        x = np.arange(self.Area[0], self.Area[1]+step, step)
        for f in func:
            plt.plot(x, f(x), label = f.__name__)
        for p in pts:
            plt.plot(p[0][0], p[0][1], '--', label = p[1])
        if legend:
            plt.legend(loc = 'best')
        plt.show()
