import time


def time_func(func):
    def timer(*args, **kwargs):
        start = time.time()
        func_result = func(*args, **kwargs)
        print(f"{func.__name__} took {(time.time() - start):.2f} seconds to execute")
        return func_result
    return timer