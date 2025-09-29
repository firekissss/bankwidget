import functools


def log(filename):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # smth before func

            result = func(*args, **kwargs)

            # smth after func

            return result

        return wrapper

    return decorator
