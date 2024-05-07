import matplotlib.pyplot as plt
import numpy as np
import inspect
import re

def return_error(func):
    """
        This function processes the input arguments to extract 'func' and 'pts' information. 
        It calculates the maximum error between the provided function values and the actual values at given points. 
        The error information is stored in the function's 'error_map'. 
        Finally, it returns the result of the input function with the processed arguments.
    """
    def wrapper(*args, **kwargs):
        
        for i in kwargs.keys():
            if i.startswith("func"):
                k = i
                break
            else:
                k = None
        if k is None:
            pass 
        else:
            func_ = kwargs[k]
        pts = []
        wrapper.error_map = {}
        for i in kwargs.keys():
            if i.startswith("pts"):
                pts.append([kwargs[i], i])
                wrapper.error_map[i] = None
        if len(pts) == 0 or k is None:
            pass
        else:
            for p in pts:
                max_ = max(abs(func_(p[0][0][i]) - p[0][1][i]) for i in range(len(p[0][0])))
                wrapper.error_map[p[1]] = max_
        
        return func(*args, **kwargs), wrapper.error_map
    wrapper.error_map = {}

    return wrapper


def re_map_pretty(error_map, sort: bool = True, sort_key = lambda item: item[1]) -> str | tuple[str, dict]:
    """
        Pretty error map (with sorting)
    """   
    sort_key = sort_key
    max_ = max(len(key) for key in error_map.keys())+5

    if sort:
        lambda_pattern  = r"lambda\s+\w+\s*:\s*.+\)\s*"
        lambda_text = re.findall(lambda_pattern, inspect.getsource(sort_key))[0][:-2]
        error_map = dict(sorted(error_map.items(), key=sort_key))
        string = f"Sorted by key -> {lambda_text}\n"

    string += '\n'.join([f'{key: <{max_}}    --->     Error: {item}' for key, item in error_map.items()])
    if sort:
        return string, error_map
    return string

def plot_histogram(error_map, digits = 5):
    """
        Plot histogram from map
        Map must be have keys, values
        keys used as labels
        values must be numeric
    """
    plt.suptitle("Histogram")
    plt.bar(error_map.keys(), error_map.values(), color = plt.cm.Set1.colors[:len(error_map.keys())])
    for i, v in enumerate(error_map.values()):
        plt.text(i, v + 0.02, f"{v:.{digits}f}", ha='center', va='bottom')
    plt.show()

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
        plt.suptitle("Plotter")
        plt.show()
