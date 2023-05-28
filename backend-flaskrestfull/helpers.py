"""
helpers.py
"""


def printify(param):
    """Printify a param

    Args:
        param (any): param to printify

    Returns:
        None
    """
    import pprint

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(param)


from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
