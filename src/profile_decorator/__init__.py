# pylint: disable = missing-module-docstring,missing-function-docstring
import cProfile
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


def profile_me(n_rows=50, sort_by="cumulative", output="stdout", filename=None):

    valid_outputs = {"stdout", "file"}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()

            # Execute the decorated function
            result = func(*args, **kwargs)

            pr.disable()
            s = io.StringIO()

            # Fallback to 'cumulative' if sort_by is invalid
            sort_by_valid = sort_by if sort_by in VALID_SORTS else "cumulative"
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by_valid)
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

            return result

        return wrapper

    # Enable the decorator to be used without parentheses if no arguments are provided
    if callable(n_rows):
        temp_func = n_rows
        n_rows = 50
        return decorator(temp_func)

    return decorator
