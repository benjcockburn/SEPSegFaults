# Tree-structured Parzen Estimator (TPE)

from scipy.stats import gaussian_kde
import numpy as np

class MinimalTPE:
    """Minimal Tree-structured Parzen Estimator (TPE)."""

    def __init__(self, bounds, n_samples=100):
        self.bounds = bounds
        self.n_samples = n_samples
        self.rng = np.random.default_rng()
        self.history = []

    def observe(self, params, value):
        self.history.append((params, value))

    def suggest(self):
        if len(self.history) < 5:
            return tuple(self.rng.uniform(low, high) for low, high in self.bounds.values())

        X = np.array([p for p, _ in self.history])
        y = np.array([v for _, v in self.history])

        # Good/bad split
        n_good = max(1, int(len(y) * 0.2))
        idx = np.argsort(y)
        X_good, X_bad = X[idx[:n_good]], X[idx[n_good:]]

        # KDEs
        self.good_kde = gaussian_kde(X_good.T)
        self.bad_kde = gaussian_kde(X_bad.T)

        candidates = self.good_kde.resample(self.n_samples).T
        l_over_g = self.good_kde.pdf(candidates.T) / (self.bad_kde.pdf(candidates.T) + 1e-12)
        best_idx = np.argmax(l_over_g)

        best_candidate = np.clip(
            candidates[best_idx],
            [b[0] for b in self.bounds.values()],
            [b[1] for b in self.bounds.values()]
        )

        return tuple(best_candidate)



def choose_next_query(spec, asked):
    """Placeholder for next query selection."""
    if spec.dims == 1:
        return (0,)
    elif spec.dims == 2:
        return (0, 0)
    else:
        return (0, 0, 0)

def generate_prediction(spec, asked):
    """Placeholder for prediction."""
    N = spec.N_array_size
    if spec.dims == 1:
        return [0.0] * N
    elif spec.dims == 2:
        return [[0.0] * N for _ in range(N)]
    else:
        return [[[0.0] * N for _ in range(N)] for _ in range(N)]
