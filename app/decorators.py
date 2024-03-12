import time
from datetime import datetime


def timeit(function):
    """
    Decorator for measuring function's execution time.
    """

    def measure_time(*args, **kw):

        caught_exception = None
        result = None

        print('Program Start:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        start_time = int(time.time())

        try:
            result = function(*args, **kw)
        except Exception as e:
            caught_exception = e

        end_time = int(time.time())
        execution_duration = (end_time - start_time)

        hours = execution_duration // 3600
        minutes = (execution_duration - 3600 * hours) // 60
        seconds = execution_duration - 3600 * hours - 60 * minutes

        print("{}Processing time of {}(): {} hours, {} minutes, {} seconds.".format(
            '\n',
            function.__qualname__,
            hours,
            minutes,
            seconds
        ))

        print('Program End:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        if caught_exception is not None:
            raise caught_exception

        return result

    return measure_time