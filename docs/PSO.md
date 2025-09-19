Particle Swarm Optimisation (PSO) Overview

A basic variant of the PSO algorithm works by having a population of candidate solutions (called particles). Each particle represents a potential solution to the optimisation problem and moves through the search space with an associated velocity. The movement of a particle is influenced both by its own best-known position (personal best) and the best-known position found by the entire swarm (global best). By iteratively updating positions and velocities, the swarm is guided toward promising regions of the search space.

The algorithm involves using a fitness function

f

that takes in a candidate solution and outputs a number that indicates the fitness of the given solution.

The goal of PSO is to find a solution m for which

f(m)<f(p)

for all p in the search space (where m is the global minimum).
This means that while PSO is not suitable to exhaustively predict the state space, it can be used to optimise which indices to query in the state space.

The Basic PSO Algorithm
	Let x∈R^n  designate a candidate solution (particle).
	Let v∈R^n  designate the velocity of the particle.
	Let NP designate the swarm size (number of particles).
	Let w designate the inertia weight, which controls how much of the previous velocity is retained.
	Let c_1,c_2 designate the cognitive and social learning factors.
	Typical settings: NP=10n (n = dimension of state space), w∈[0.5,0.9], c_1=c_2=2.

Initialisation:
	Initialise all particles x with random positions in the state space.
	Initialise all velocities v with small random values.
	Record each particle’s initial personal best (pbest) as its starting position.
	Record the best solution found across the swarm (gbest).

Evolutionary loop (until termination criteria met, e.g. max iterations):

For each particle in the swarm:

	Update velocity for each dimension i∈{1,….,n}:
        v_i=wv_i+c_1 r_1 (〖pbest〗_i-x_i )+c_2 r_2 (〖gbest〗_i-x_i)
    where r_1,r_2~U(0,1) are random coefficients.

	Update position:
        x_i=x_i+v_i
	Evaluate fitness: If f(x) improves the personal best, update pbest.
	If any particle improves upon the global best, update gbest.

Integrating into the Inovor Project:

The pyswarm library or the pyswarms package in Python provide convenient implementations of PSO, which could be adapted to the project.
	pyswarm
	pyswarms

Potential Program Flow (PSO for Query Selection):

	Parse Inputs
	    dimensions (1, 2, or 3)
	    array_size (length of each dimension)
	    max_queries (query budget)

	Initialize State Representation
	    Create an empty structure to store discovered truth values (array, matrix, or tensor).

	Query Selection (PSO)
	    Candidate solution = a set of query indices (max queries many).
	    Particles explore sets of query indices by updating positions and velocities.

	Evolutionary Loop
	    PSO iteratively refines candidate sets of query indices until a query plan emerges.
	Execution
	    Once the plan is fixed, run the queries, then fill in the rest.

	Prediction Phase
	    Once budget is exhausted, fill in the rest of the state-space with predictions.
	    Strategies:
	        Interpolation (nearest-neighbor, spline, kriging)
	        Model fitting (regression, GP surrogate, neural net trained on sampled points)
	        Black-box optimiser to minimise reconstruction error.
	Submit Prediction
	    Output full state-space prediction.

Video that helps with understanding (cool visuals especially if you like finding nemo):
https://www.youtube.com/watch?v=2yKI3wKOWyc 

Verification
Unfortunately, due to the nature of the PSO interpolation being primarily used for finding a specific point in the state space rather than exploring the state space as a whole, PSO investigation and implementation will be discontinued.  