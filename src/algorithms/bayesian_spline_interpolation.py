"""
Bayesian Spline Interpolation algorithm module.
https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html
"""
from typing import List, Tuple
import numpy as np
try:
    from scipy.interpolate import BSpline
    _HAVE_SCIPY = True
except Exception:
    _HAVE_SCIPY = False

def _evenly_spaced_indices(N: int, Q: int) -> List[int]:
    if Q <= 1:
        return [N // 2]
    xs = []
    for i in range(Q):
        x = round(i * (N - 1) / max(Q - 1, 1))
        xs.append(int(x))
    seen, out = set(), []
    for v in xs:
        if v not in seen:
            out.append(v); seen.add(v)
    return out

def choose_next_query(spec, asked):
    N = spec.N_array_size
    Q = spec.Queries
    plan = _evenly_spaced_indices(N, Q if spec.dims == 1 else max(4, Q))
    asked_set = {a.index for a in asked}

    def first_unasked_1d():
        for i in plan:
            if (i,) not in asked_set:
                return (i,)
        for i in range(N):
            if (i,) not in asked_set:
                return (i,)
        return (0,)

    def first_unasked_2d():
        for i in plan:
            if (i, i) not in asked_set:
                return (i, i)
        for i in range(N):
            for j in range(N):
                if (i, j) not in asked_set:
                    return (i, j)
        return (0, 0)

    def first_unasked_3d():
        for i in plan:
            if (i, i, i) not in asked_set:
                return (i, i, i)
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if (i, j, k) not in asked_set:
                        return (i, j, k)
        return (0, 0, 0)

    if spec.dims == 1: return first_unasked_1d()
    if spec.dims == 2: return first_unasked_2d()
    return first_unasked_3d()

def generate_prediction(spec, asked):
    N = spec.N_array_size
    if spec.dims == 1:
        y_hat = _fit_pspline_mean_1d(
            N=N,
            asked=asked,
            degree=3,
            n_bases=min(10, N),
            lam=10.0,  # will tune/learn in a later commit
        )
        return [float(v) for v in y_hat]
    if spec.dims == 2:
        # placeholder until next commit: zeros
        return [[0.0] * N for _ in range(N)]
    # dims == 3
    return [[[0.0] * N for _ in range(N)] for _ in range(N)]

def _uniform_knots(n_points: int, degree: int, n_bases: int):
    # Domain is integer grid x = 0..N-1
    x_min, x_max = 0.0, float(n_points - 1)
    # Build clamped knot vector with uniform interior knots
    n_interior = max(n_bases - degree - 1, 0)
    if n_interior > 0:
        interior = np.linspace(x_min, x_max, n_interior + 2)[1:-1]
        knots = np.concatenate((
            np.repeat(x_min, degree + 1),
            interior,
            np.repeat(x_max, degree + 1),
        ))
    else:
        knots = np.concatenate((
            np.repeat(x_min, degree + 1),
            np.repeat(x_max, degree + 1),
        ))
    return knots

def _bspline_design_matrix_1d(N: int, degree: int = 3, n_bases: int = 10):
    n_bases = int(min(max(n_bases, degree + 1), N))  # clamp
    x = np.arange(N, dtype=float)
    if _HAVE_SCIPY:
        t = _uniform_knots(N, degree, n_bases)
        # Build each basis column by using one-hot coefficients
        cols = []
        for k in range(n_bases):
            c = np.zeros(n_bases)
            c[k] = 1.0
            bs = BSpline(t, c, degree, extrapolate=True)
            cols.append(bs(x))
        Phi = np.column_stack(cols)
    else:
        # Graceful fallback: polynomial (Vandermonde) basis up to degree p
        # (not truly a B-spline, but lets the pipeline run without SciPy)
        p = min(degree, n_bases - 1)
        Phi = np.vander(x / max(N - 1, 1.0), N=p + 1, increasing=True)
        # pad to n_bases if needed
        if Phi.shape[1] < n_bases:
            Phi = np.pad(Phi, ((0, 0), (0, n_bases - Phi.shape[1])), mode='constant')
    return Phi  # shape (N, n_bases)

def _second_difference_penalty(n_bases: int):
    # D: (n_bases - 2) x n_bases with rows [.. 1 -2 1 ..]
    if n_bases < 3:
        return np.eye(n_bases)
    D = np.zeros((n_bases - 2, n_bases))
    for i in range(n_bases - 2):
        D[i, i:i+3] = [1.0, -2.0, 1.0]
    Q = D.T @ D
    return Q


def _fit_pspline_mean_1d(N: int, asked, degree=3, n_bases=10, lam=10.0):
    # Build design matrix on full grid and select observed rows
    Phi_full = _bspline_design_matrix_1d(N, degree=degree, n_bases=n_bases)
    Q = _second_difference_penalty(Phi_full.shape[1])

    if len(asked) == 0:
        # No data: return zeros for now (could return prior mean)
        return np.zeros(N)

    obs_idx = np.array([a.index[0] for a in asked], dtype=int)
    y = np.array([a.value for a in asked], dtype=float)

    Phi_obs = Phi_full[obs_idx, :]  # (n_obs, K)
    K = Phi_full.shape[1]

    # Solve (Phi^T Phi + lam Q) beta = Phi^T y
    A = Phi_obs.T @ Phi_obs + lam * Q
    b = Phi_obs.T @ y
    # Regularize if singular
    eps = 1e-8
    A = A + eps * np.eye(K)
    beta = np.linalg.solve(A, b)

    y_hat = Phi_full @ beta  # (N,)
    return y_hat
