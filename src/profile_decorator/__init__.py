"""profile decorator definition"""

# pylint: disable = missing-function-docstring
import asyncio
import cProfile
import logging
import pstats
from pstats import SortKey
import io
from functools import wraps

VALID_SORTS = set(
    val
    for name, attribute in SortKey.__dict__.items()
    if not name.startswith("__") and isinstance(attribute, tuple)
    for val in attribute
)


def profile(n_rows=50, sort_by="cumulative", output="stdout", filename=None):

    valid_outputs = {"stdout", "file", "log"}

    def decorator(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with cProfile.Profile() as pr:
                # Directly await the async function here
                result = await func(*args, **kwargs)
                process_profiling_results(pr)

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with cProfile.Profile() as pr:
                result = func(*args, **kwargs)
                process_profiling_results(pr)

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    def process_profiling_results(pr):
        s = io.StringIO()
        # Fallback to 'cumulative' if sort_by is invalid
        if isinstance(sort_by, (list, tuple)):
            sort_by_valid = [s for s in sort_by if s in VALID_SORTS]
        else:
            sort_by_valid = [sort_by] if sort_by in VALID_SORTS else ["cumulative"]

        ps = pstats.Stats(pr, stream=s).sort_stats(*sort_by_valid)
        ps.print_stats(n_rows)

        # Handle output
        if output not in valid_outputs:
            raise ValueError(
                f"Invalid output option '{output}'. Valid options are {valid_outputs}."
            )

        if output == "stdout":
            print(s.getvalue())
        elif output == "file":
            if not filename:
                raise ValueError("Filename must be provided when output is 'file'.")
            try:
                with open(filename, "w+", encoding="utf-8") as f:
                    f.write(s.getvalue())
            except IOError as e:
                raise IOError(f"Error writing to file {filename}: {e}") from e
        elif output == "log":
            logger = logging.getLogger(__name__)
            logger.info(s.getvalue())
        else:
            raise ValueError("'output' must be one of 'stdout', 'file' or 'log'.")

    # Enable the decorator to be used without parentheses if no arguments are provided
    if callable(n_rows):
        temp_func = n_rows
        n_rows = 50
        return decorator(temp_func)

    return decorator
