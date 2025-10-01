import numpy as np
from scipy.linalg import lstsq
from scipy.stats import norm


def choose_next_query(spec, asked):
    """
    Bayesian Quadratic Interpolation query strategy:
    Select the next query point where the predicted uncertainty (variance)
    is largest, based on a quadratic surrogate model.
    """
    N = spec.N_array_size
    dims = spec.dims

    # If no samples yet, pick middle point(s)
    if not asked:
        mid = (N - 1) // 2
        if dims == 1:
            return (mid,)
        elif dims == 2:
            return (mid, mid)
        else:
            return (mid, mid, mid)

    # Build coordinate grid for all possible points
    if dims == 1:
        grid = np.arange(N).reshape(-1, 1)
    elif dims == 2:
        grid = np.array([(i, j) for i in range(N) for j in range(N)])
    else:
        grid = np.array([(i, j, k) for i in range(N) for j in range(N) for k in range(N)])

    # Extract training data
    X = np.array([q.index for q in asked])
    y = np.array([q.value for q in asked])

    # Fit a quadratic model to data
    Phi = _design_matrix(X)
    coeffs, _, _, _ = lstsq(Phi, y)

    # Predict mean and uncertainty over all grid points
    Phi_all = _design_matrix(grid)
    y_pred = Phi_all @ coeffs

    # Estimate variance based on residuals
    residuals = y - Phi @ coeffs
    sigma = np.std(residuals) if len(residuals) > 1 else 1.0

    # Add exploration factor (random Gaussian noise proportional to uncertainty)
    acquisition = np.abs(np.random.normal(y_pred, sigma))

    # Mask out already-queried points
    asked_indices = {tuple(q.index) for q in asked}
    available = [tuple(pt) for pt in grid if tuple(pt) not in asked_indices]
    available_scores = [acquisition[i] for i, pt in enumerate(grid) if tuple(pt) not in asked_indices]

    # Pick the highest-acquisition point
    best_idx = np.argmax(available_scores)
    return available[best_idx]


def generate_prediction(spec, asked):
    """
    Generate a full-state prediction using the fitted quadratic model.
    """
    N = spec.N_array_size
    dims = spec.dims

    if not asked:
        # No data -> uniform zero
        if dims == 1:
            return [0.0] * N
        elif dims == 2:
            return [[0.0] * N for _ in range(N)]
        else:
            return [[[0.0] * N for _ in range(N)] for _ in range(N)]

    X = np.array([q.index for q in asked])
    y = np.array([q.value for q in asked])

    # Fit quadratic model
    Phi = _design_matrix(X)
    coeffs, _, _, _ = lstsq(Phi, y)

    # Predict mean values on full grid
    if dims == 1:
        grid = np.arange(N).reshape(-1, 1)
        y_pred = _design_matrix(grid) @ coeffs
        return y_pred.tolist()

    elif dims == 2:
        y_pred = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                Phi_ij = _design_matrix(np.array([[i, j]]))
                y_pred[i, j] = (Phi_ij @ coeffs)[0]
        return y_pred.tolist()

    else:
        y_pred = np.zeros((N, N, N))
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    Phi_ijk = _design_matrix(np.array([[i, j, k]]))
                    y_pred[i, j, k] = (Phi_ijk @ coeffs)[0]
        return y_pred.tolist()


# ---------------- Helper: quadratic feature expansion ----------------

def _design_matrix(X):
    """
    Construct a quadratic design matrix for input X.
    Each row includes bias, linear, and quadratic terms.
    """
    n, d = X.shape
    features = []

    # Bias term
    features.append(np.ones((n, 1)))

    # Linear terms
    features.append(X)

    # Quadratic and cross terms
    for i in range(d):
        for j in range(i, d):
            term = (X[:, i] * X[:, j]).reshape(-1, 1)
            features.append(term)

    # Concatenate all features horizontally
    Phi = np.hstack(features)
    return Phi

