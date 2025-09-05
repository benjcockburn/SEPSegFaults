"""
Blank algorithm module.

You can copy this file, rename it (e.g., my_algorithm.py),
and implement your own query strategy + prediction generator.

Import into titan_client.py as:
    from algorithms import blank_algorithm
"""

def choose_next_query(spec, asked):
    """
    Decide the next index to query.
    Arguments:
        spec  - ProblemSpec (dims, N, Q)
        asked - list of QueryResult objects already queried
    Return:
        A tuple (i,), (i,j), or (i,j,k) depending on spec.dims

    TODO: Replace with your own query logic.
    """
    # Example placeholder: always return (0,), (0,0), or (0,0,0)
    if spec.dims == 1:
        return (0,)
    elif spec.dims == 2:
        return (0, 0)
    else:
        return (0, 0, 0)


def generate_prediction(spec, asked):
    """
    Build a prediction for the entire state space.
    Arguments:
        spec  - ProblemSpec (dims, N, Q)
        asked - list of QueryResult objects already queried
    Return:
        A nested list:
            dims=1 -> [N]
            dims=2 -> [[N] * N]
            dims=3 -> [[[N] * N for j] for i]

    TODO: Replace with your own prediction logic.
    """
    N = spec.N_array_size
    if spec.dims == 1:
        return [0.0] * N
    if spec.dims == 2:
        return [[0.0] * N for _ in range(N)]
    return [[[0.0] * N for _ in range(N)] for _ in range(N)]
