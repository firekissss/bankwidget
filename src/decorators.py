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


def log_exceptions(logger):
    """
    Decorator that automatically logs any unhandled exceptions raised within the wrapped function.

    When an exception occurs, it is logged with ERROR level (including the full stack trace)
    using the provided logger, and then re-raised to preserve the original behavior.

    Parameters
    ----------
    logger : logging.Logger
        The logger instance used to record error messages.

    Returns
    -------
    Callable
        A decorator that wraps the target function with automatic exception logging.

    Raises
    ------
    Exception
        Any exception raised inside the wrapped function is logged and re-raised.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(str(e))
                raise

        return wrapper

    return decorator
