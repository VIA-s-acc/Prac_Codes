import matplotlib.pyplot as plt
import numpy as np
class Plotter():
    """
        Class for plotting MPE
    """

    def __init__(self, Area):
        self.Area = Area

    def plot(self, **kwargs):
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
                pts.append(kwargs[i])
        x = np.arange(self.Area[0], self.Area[1], step)
        for f in func:
            plt.plot(x, f(x))
        for p in pts:
            plt.plot(p[0], p[1], '--')
        plt.show()
