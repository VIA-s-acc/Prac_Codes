import matplotlib.pyplot as plt
import numpy as np
import inspect
import re
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import random
from warnings import warn

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
                func* (list, optional): List of functions. 
                pts* (list, optional): List of points. 
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

    def plot_solution(self, T, L, **kwargs):
        """
            Plot solution
        Args:
            T (float): Total time period
            L (float): Length of the domain
            - **kwargs:
                - func* (list, optional): List of functions. 
                - pts* (list, optional): 2D Array of points chain. 
                - legend (bool, optional): Legend. Defaults to True.
                - func* means func1, func2, func3, ... or something else
                - pts* means pts1, pts2, pts3, ... or something else
                - edgecolor (str, optional): Edge color. Defaults to 'none'.
                - step_x (float, optional): Step x. Defaults to 0.1.
                - step_t (float, optional): Step t. Defaults to 0.1.

        Example:
        -------
        plotter = Plotter(Area = (0, L), T = T, N = N, M = M)
        plotter.plot_solution(T = T, L = L, N = N, M = M, func1 = func1, func2 = func2, pts1 = pts1, pts2 = pts2)

        Notes:
        -------
            If no functions or points are given, nothing will be plotted, returned value will be False, and a warning will be shown.

        Returns:
            bool: if functions or points are given, returned value will be True, otherwise False
        """


        
        fig = plt.figure()
        count = 0
        for key in kwargs.keys():
            if key.startswith("func") or key.startswith("pts"):
                count += 1
        
        if count == 0:
            warn("No functions or points")
            return False
        else:
            rows = count // 2
            if rows == 0:
                rows = 1
            if count >= 3:
                plots = rows * 100 + 31
            elif count == 2:
                plots = rows * 100 + 21
            else:
                plots = 100 + 11
            i = 0
            print(plots)
        if 'legend' in kwargs.keys():
            legend = kwargs['legend']
            if type(legend) != type(False):
                legend = True
        else:
            legend = True
        color = 'none'
        colors = plt.cm.Set1.colors + ('blue', 'red', 'green', 'yellow', 'purple', 'cyan', 'magenta', 'orange', 'brown', 'black', 'gray', 'lightgray', 'darkgray', 'white', 'none', 'random')
        if 'edgecolor' in kwargs.keys():
            edgecolor = kwargs['edgecolor']
            if edgecolor in colors:
                color = edgecolor
            else:
                warn(f"{edgecolor} is not in {colors}", category=SyntaxWarning)
                warn("set edgecolor = 'none'", category=SyntaxWarning)
        else:
            edgecolor = 'none'
        if 'step_x' in kwargs.keys():
            step_x = kwargs['step_x']
            if type(step_x) != type(0.1):
                step_x = 0.1
                warn("step_x must be int or float", category=SyntaxWarning)
                warn("set step_x = 0.1", category=SyntaxWarning)
        else:
            step_x = 0.1
        if 'step_t' in kwargs.keys():
            step_t = kwargs['step_t']
            if type(step_t) != type(0.1):
                step_t = 0.1
                warn("step_t must be int or float", category=SyntaxWarning)
                warn("set step_t = 0.1", category=SyntaxWarning)
        else:
            step_t = 0.1
        for key in kwargs.keys():
            if edgecolor == "random":
                color = random.choice(colors)
                while color == "random":
                    color = random.choice(colors)
            if key.startswith("func"):
                ax = fig.add_subplot(plots + i, projection='3d')
                X_ = np.linspace(0, L, int(L/step_x))
                T_ = np.linspace(0, T, int(T/step_t))
                X_, T_ = np.meshgrid(X_, T_)
                ax.plot_surface(X_, T_, kwargs[key](X_, T_), cmap='viridis', edgecolor=color, label=key)
                if legend == True:
                    ax.legend(loc = 'best')
            if key.startswith("pts"):
                u = np.array(kwargs[key])
                X_ = np.linspace(0, L, len(u[0]) )
                T_ = np.linspace(0, T, len(u) )
                X_, T_ = np.meshgrid(X_, T_)
                ax = fig.add_subplot(plots + i, projection='3d')
                ax.plot_surface(X_, T_, u, cmap='viridis', edgecolor=color, label=key)
                if legend == True:
                    ax.legend(loc = 'best')
            i+=1
                
            
        
        if legend == True:
            fig.legend(labels = kwargs.keys())
        
    

        ax.set_xlabel('x')
        ax.set_ylabel('t')
        ax.set_zlabel('u(x, t)')
        plt.show()
        return True

    

   