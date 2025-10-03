import sys, os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/algorithms')))
from bayesian_quadratic import choose_next_query, generate_prediction

# Dummy TITAN-style classes
class ProblemSpec:
    def __init__(self, dims, N, Q):
        self.dims = dims
        self.N_array_size = N
        self.Queries = Q

class QueryResult:
    def __init__(self, index, value):
        self.index = index
        self.value = value

# --------------------------------------------------------------------
# 1D Test: Quadratic f(x) = (x - 2)^2
# --------------------------------------------------------------------
def test_1d_quadratic():
    spec = ProblemSpec(1, N=5, Q=5)
    true_func = lambda x: (x - 2)**2

    asked = []
    for _ in range(spec.Queries):
        idx = choose_next_query(spec, asked)
        val = true_func(idx[0])
        asked.append(QueryResult(idx, val))

    pred = generate_prediction(spec, asked)
    print("1D prediction:", np.round(pred, 3))
    print("1D next query sequence:", [a.index for a in asked])

# --------------------------------------------------------------------
# 2D Test: f(x,y) = (x - 2)^2 + (y - 1)^2
# --------------------------------------------------------------------
def test_2d_paraboloid():
    spec = ProblemSpec(2, N=5, Q=8)
    true_func = lambda x, y: (x - 2)**2 + (y - 1)**2

    asked = []
    for _ in range(spec.Queries):
        idx = choose_next_query(spec, asked)
        val = true_func(idx[0], idx[1])
        asked.append(QueryResult(idx, val))

    pred = np.array(generate_prediction(spec, asked))
    print("2D prediction (center slice):")
    print(np.round(pred, 2))
    print("2D next query sequence:", [a.index for a in asked])

# --------------------------------------------------------------------
# 3D Test: f(x,y,z) = (x-1)^2 + (y-2)^2 + (z-3)^2
# --------------------------------------------------------------------
def test_3d_paraboloid():
    spec = ProblemSpec(3, N=4, Q=10)
    true_func = lambda x, y, z: (x - 1)**2 + (y - 2)**2 + (z - 3)**2

    asked = []
    for _ in range(spec.Queries):
        idx = choose_next_query(spec, asked)
        val = true_func(idx[0], idx[1], idx[2])
        asked.append(QueryResult(idx, val))

    pred = np.array(generate_prediction(spec, asked))
    print("3D prediction slice (z=0):")
    print(np.round(pred[:, :, 0], 2))
    print("3D next query sequence:", [a.index for a in asked])

# --------------------------------------------------------------------
# Random surface sanity test: f(x,y) = sin(x) + cos(y)
# --------------------------------------------------------------------
def test_random_surface():
    spec = ProblemSpec(2, N=6, Q=10)
    true_func = lambda x, y: np.sin(x) + np.cos(y)

    asked = []
    for _ in range(spec.Queries):
        idx = choose_next_query(spec, asked)
        val = true_func(idx[0], idx[1])
        asked.append(QueryResult(idx, val))

    pred = np.array(generate_prediction(spec, asked))
    print("Random surface (approx):")
    print(np.round(pred, 2))
    print("Query count:", len(asked))

# --------------------------------------------------------------------
if __name__ == "__main__":
    print("===== TEST 1: 1D QUADRATIC =====")
    test_1d_quadratic()
    print("\n===== TEST 2: 2D PARABOLOID =====")
    test_2d_paraboloid()
    print("\n===== TEST 3: 3D PARABOLOID =====")
    test_3d_paraboloid()
    print("\n===== TEST 4: RANDOM SURFACE =====")
    test_random_surface()
