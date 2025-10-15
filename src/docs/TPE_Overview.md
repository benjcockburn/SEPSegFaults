# Tree-Structured Parzen Estimator (TPE)

## Overview

The **Tree-structured Parzen Estimator (TPE)** is a form of **Bayesian optimisation** that models how likely parameter configurations are to yield good performance. It provides a balance between **exploration** (trying new regions) and **exploitation** (focusing on known good regions), without requiring complex Gaussian Process regression.

TPE is computationally lightweight, robust to noise, and well-suited for higher-dimensional or mixed-variable optimisation problems.

---

## Core Idea

Unlike Gaussian Process BO, which models the objective distribution **p(y | x)**, TPE models the inverse distribution **p(x | y)** and separates observations into:

- **Good observations (l)** — points where the objective value is below a quantile threshold γ.
- **Bad observations (g)** — points above that threshold.

The algorithm then samples candidate points from the **“good” distribution** and chooses those that maximise the ratio:

\[
\text{EI}(x) \propto \frac{l(x)}{g(x)}
\]

This ratio approximates the **expected improvement**—it favours regions where the density of good configurations is high but bad configurations are low.

---

## Algorithm Steps

1. **Initialisation:**  
   Randomly sample several points to populate the history.

2. **Partitioning:**  
   Sort all evaluated points by their objective value and split them into two groups:
   - Top γ fraction → "good"
   - Rest → "bad"

3. **Density Estimation:**  
   Fit **Kernel Density Estimators (KDEs)** to both good and bad sets.

4. **Sampling:**  
   Draw candidate samples from the good KDE and compute the likelihood ratio \( l(x) / g(x) \).

5. **Selection:**  
   Choose the sample with the highest ratio as the next candidate.

6. **Observation:**  
   Evaluate the objective at that point and record the result.

Repeat until the evaluation budget is exhausted.

---

## Advantages

| Feature | Description |
|----------|--------------|
| **No matrix inversions** | Unlike Gaussian Processes, TPE scales linearly with sample count. |
| **Handles mixed variables** | Works with continuous, categorical, and discrete spaces. |
| **Easy integration** | Can directly plug into existing black-box optimisation pipelines. |
| **Computationally light** | Only uses simple density estimation and sampling. |

---

## Integration into `SEPSegFaults`

The `TPEOptimizer` class can be used as a drop-in replacement for your existing optimisers (e.g., linear or polynomial).

Typical usage pattern:

```python
from algorithms.tpe_optimizer import TPEOptimizer

optimizer = TPEOptimizer(bounds={"x1": (-5, 5), "x2": (0, 3)})

for step in range(N):
    params = optimizer.suggest()
    result = objective_function(params)
    optimizer.observe(params, result)
