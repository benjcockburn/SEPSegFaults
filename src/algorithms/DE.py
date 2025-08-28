import sys
import numpy as np
from scipy.optimize import differential_evolution

def main():
    # Parse inputs
    dimensions = int(sys.argv[1])
    array_size = int(sys.argv[2])
    max_queries = int(sys.argv[3])

    shape = tuple([array_size] * dimensions)
    discovered = np.full(shape, np.nan)

    # Use Differential Evolution to plan queries
    query_plan = plan_queries(dimensions, array_size, max_queries)

    # Execute queries
    for idx in query_plan:
        idx = tuple(int(i) for i in idx)
        value = query_truth(idx)   # black-box truth oracle
        discovered[idx] = value

    # Reconstruct full state space
    prediction = fill_missing(discovered)

    # Submit final prediction
    submit_prediction(prediction)


# ---------------- Differential Evolution Part ---------------- #

def plan_queries(dimensions, array_size, max_queries):
    """
    Use DE to select query indices.
    Each candidate is a flat vector of size (max_queries * dimensions).
    """
    bounds = [(0, array_size - 1)] * (max_queries * dimensions)

    def fitness(candidate):
        # Candidate -> reshape into query points
        points = np.array(candidate).reshape(max_queries, dimensions).astype(int)

        # Proxy fitness: maximize spread (coverage of state space)
        # Compute average pairwise distance between query points
        dists = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dists.append(np.linalg.norm(points[i] - points[j]))
        return -np.mean(dists)  # negative because DE minimizes

    result = differential_evolution(fitness, bounds, maxiter=50, popsize=15, disp=True)
    best_points = np.array(result.x).reshape(max_queries, dimensions)
    return best_points


# ----------------- Utility Methods ----------------- #

def query_truth(idx):
    # Placeholder: in practice, call hidden system
    # For testing, simulate a function
    return np.sum(idx)  # e.g. truth = sum of coordinates

def fill_missing(discovered):
    # Fill missing values with mean of known entries
    mean_val = np.nanmean(discovered)
    return np.nan_to_num(discovered, nan=mean_val)

def submit_prediction(prediction):
    # For now, just print shape
    print("Prediction shape:", prediction.shape)


if __name__ == "__main__":
    main()