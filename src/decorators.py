import datetime
import functools
import traceback


def log(filename=None):
    """
    Decorator that logs function calls with timestamp, arguments,
    return value, and errors.

    Parameters
    ----------
    filename : str or None, optional
        Path to a log file. If None, logs are printed to the console.

    Returns
    -------
    function
        Wrapped function with logging enabled.

    Raises
    ------
    Exception
        Re-raises any exception raised by the wrapped function after logging it.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # smth before func
            call_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            log_text = [f"[{call_time}] Function '{func.__name__}' called"]
            try:
                log_text.append(f"args: {args}\nkwargs: {kwargs}")
                result = func(*args, **kwargs)
                log_text.append(f"result: {result}")
            except Exception as e:
                log_text.append(f"error: {e}")
                log_text.append(traceback.format_exc())
                result = None
                raise
            finally:
                if filename is None:
                    print("\n".join(log_text))
                else:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write("\n".join(log_text) + "\n\n")
            return result

        return wrapper

    return decorator
