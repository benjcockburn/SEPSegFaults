#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# TITAN client scaffold (single file, verbose, no algorithms).
#
# This program:
#   1) Parses three integer command-line arguments:
#        - dims:       number of dimensions (1, 2, or 3)
#        - array_size: N, the size of each dimension
#        - max_queries: Q, how many queries we may ask before predicting
#   2) Repeatedly:
#        - Chooses an index to query (YOU provide the strategy)
#        - Writes the query to stdout and flushes immediately
#        - Reads a float response from stdin (the “truth” at that index)
#      until Q valid queries have been recorded.
#   3) Outputs a single prediction line for the entire state space, exactly in
#      the format the platform expects.
#
# IMPORTANT:
#   - Do not print anything except queries and the final prediction to stdout.
#   - Keep your algorithms OUT of this file. Use the two hook functions:
#       choose_next_query(...)
#       generate_prediction(...)
#   - Use ./algorithms directory and 
#    from algorithms import YOUR_ALGORITHM_NAME i.e"
from algorithms import bayesian_spline_interpolation as template_algorithm
# -----------------------------------------------------------------------------

import sys
from typing import List, Tuple, Any, Optional


# ------------------------------ Data holders ---------------------------------

class ProblemSpec:
    """
    Holds the input specification so we can pass it around clearly.
    """
    def __init__(self, dims: int, array_size: int, max_queries: int):
        self.dims = dims            # 1, 2, or 3
        self.N_array_size = array_size         # size per dimension
        self.Queries = max_queries        # how many queries allowed


class QueryResult:
    """
    Records a single successful query: the index we asked for and the float
    value we received from the platform.
    """
    def __init__(self, index: Tuple[int, ...], value: float):
        self.index = index          # (i,), (i,j), or (i,j,k)
        self.value = value          # truth value returned for that index


# ------------------------------- Hook points ----------------------------------

def choose_next_query(spec, asked):
    # change for your algorithm, make sure to import it before changing the base object
    return template_algorithm.choose_next_query(spec, asked) 

def generate_prediction(spec, asked):
    return template_algorithm.generate_prediction(spec, asked)

# ------------------------------- I/O helpers ----------------------------------

def write_query_to_stdout(index: Tuple[int, ...]) -> None:
    """
    Output a single query line to stdout in the exact format TITAN expects,
    then flush immediately so the platform can respond.
      - 1D: "i"
      - 2D: "i,j"
      - 3D: "i,j,k"
    """
    if len(index) == 1:
        line = f"{index[0]}"
    elif len(index) == 2:
        line = f"{index[0]},{index[1]}"
    else:
        line = f"{index[0]},{index[1]},{index[2]}"

    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def read_float_from_stdin() -> Optional[float]:
    """
    Read one line from stdin and try to parse it as a float. If parsing fails,
    it likely means the platform printed an error message (e.g., invalid query),
    so we return None. The caller will then try a different index.
    """
    line = sys.stdin.readline()
    if not line:
        return None  # EOF or no response

    stripped = line.strip()
    try:
        value = float(stripped)
        return value
    except ValueError:
        # Probably an error message string from the platform; treat as invalid.
        return None


def flatten_prediction_to_one_line(spec: ProblemSpec, pred: Any) -> str:
    """
    Convert the nested prediction structure into a single space-separated line
    in the order TITAN requires:

      - 1D: N floats
      - 2D: N rows, each with N floats, row-major (i then j), all on one line
      - 3D: N "columns" along k, where each column is a 2D block emitted in
            row-major. The order is:
              for k in 0..N-1:
                for i in 0..N-1:
                  for j in 0..N-1:
                    yield pred[i][j][k]
    """
    N = spec.N_array_size
    pieces: List[str] = []

    if spec.dims == 1:
        i = 0
        while i < N:
            number = float(pred[i])
            pieces.append(str(number))
            i = i + 1
        return " ".join(pieces)

    if spec.dims == 2:
        i = 0
        while i < N:
            j = 0
            while j < N:
                number = float(pred[i][j])
                pieces.append(str(number))
                j = j + 1
            i = i + 1
        return " ".join(pieces)

    # dims == 3
    k = 0
    while k < N:
        i = 0
        while i < N:
            j = 0
            while j < N:
                number = float(pred[i][j][k])
                pieces.append(str(number))
                j = j + 1
            i = i + 1
        k = k + 1
    return " ".join(pieces)


def parse_command_line_arguments(argv: List[str]) -> ProblemSpec:
    """
    Convert argv into a ProblemSpec. Exits with code 2 and a helpful message
    if the arguments are missing or invalid.
    """
    # Expect exactly 3 extra arguments: dims, array_size, max_queries
    if len(argv) != 4:
        sys.stderr.write(
            "Usage: python titan_client.py <dims:1|2|3> <array_size:N> <max_queries:Q>\n"
        )
        sys.exit(2)

    # Try to parse them as integers
    try:
        dims = int(argv[1])
        array_size = int(argv[2])
        max_queries = int(argv[3])
    except ValueError:
        sys.stderr.write("All arguments must be integers.\n")
        sys.exit(2)

    # Validate ranges
    if dims not in (1, 2, 3):
        sys.stderr.write("dims must be 1, 2, or 3.\n")
        sys.exit(2)

    if array_size < 1:
        sys.stderr.write("array_size must be >= 1.\n")
        sys.exit(2)

    if max_queries < 0:
        sys.stderr.write("max_queries must be >= 0.\n")
        sys.exit(2)

    return ProblemSpec(dims=dims, array_size=array_size, max_queries=max_queries)


# ---------------------------------- Main --------------------------------------

def main(argv: List[str]) -> int:
    """
    Drives the whole interaction:
      - parse args → spec
      - query loop until Q valid responses recorded
      - build prediction → flatten → print once
    """
    spec = parse_command_line_arguments(argv)

    # Keep a list of successful queries (index + returned value).
    successful_queries: List[QueryResult] = []

    # Continue until we've collected exactly Q valid query results.
    while len(successful_queries) < spec.Queries:
        # 1) Ask our hook to choose an index (YOU replace the policy).
        next_index = choose_next_query(spec, successful_queries)

        # 2) Validate the shape and bounds of the index before sending it.
        #    If it's invalid, skip emitting and choose again.
        if len(next_index) != spec.dims:
            # Wrong number of coordinates; try selecting another index.
            continue

        all_in_bounds = True
        for coordinate in next_index:
            if coordinate < 0 or coordinate >= spec.N_array_size:
                all_in_bounds = False
                break
        if not all_in_bounds:
            continue

        # 3) Emit the query exactly as required and flush immediately.
        write_query_to_stdout(next_index)

        # 4) Read one response line. If it isn't a float, this query didn't count
        #    (platform prints an error message) so we simply try again.
        maybe_value = read_float_from_stdin()
        if maybe_value is None:
            # Invalid query from platform’s perspective; do not count it.
            # Loop will try again.
            continue

        # 5) We have a valid float. Record it.
        record = QueryResult(index=next_index, value=maybe_value)
        successful_queries.append(record)

    # At this point, we have exactly Q valid query results recorded.

    # 6) Build a full-size prediction structure (shape depends on dims).
    prediction_structure = generate_prediction(spec, successful_queries)

    # 7) Flatten the prediction into a single line in the required order.
    prediction_line = flatten_prediction_to_one_line(spec, prediction_structure)

    # 8) Output the prediction line and flush.
    sys.stdout.write(prediction_line + "\n")
    sys.stdout.flush()

    return 0


if __name__ == "__main__":
    # Delegate to main and use the exit code it returns.
    exit_code = main(sys.argv)
    raise SystemExit(exit_code)
