import time

def time_decorator(func):
    """
    A decorator function that measures the execution time of the input function and prints the time taken. 
    Takes in a function as input and returns a wrapper function. 
    """
    def wrapper(*args, **kwargs):
        """
        This function acts as a wrapper for another function, timing its execution and printing the duration. 
        It takes any number of positional and keyword arguments and returns the result of the wrapped function. 
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper
