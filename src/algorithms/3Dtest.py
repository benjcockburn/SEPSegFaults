import sys
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, RBF
# import math

def gp_3d_reconstruction(points, values, grid_shape=(20, 20, 20), kernel_type="Matern"):
    """
    Perform 3D Gaussian Process Regression (Kriging) on scattered data 
    and reconstruct a full 3D grid.

    Parameters
    ----------
    points : ndarray of shape (N, 3)
        Scattered input points in 3D.
    values : ndarray of shape (N,)
        Scalar values at the input points.
    grid_shape : tuple of ints (Nx, Ny, Nz)
        Shape of the output 3D grid.
    kernel_type : str
        Kernel to use: "Matern" or "RBF".

    Returns
    -------
    grid_x, grid_y, grid_z : 3D meshgrids
    mean_grid : ndarray of shape grid_shape
        Predicted mean values on the 3D grid.
    std_grid : ndarray of shape grid_shape
        Predicted standard deviation (uncertainty).
    """
    # Select kernel
    if kernel_type == "Matern":
        kernel = 1.0 * Matern(length_scale=1.0, nu=1.5)
    else:
        kernel = 1.0 * RBF(length_scale=1.0)

    # Fit GP model
    gp = GaussianProcessRegressor(kernel=kernel, alpha=0.01, n_restarts_optimizer=5, normalize_y=True)
    gp.fit(points, values)

    # Build 3D grid
    Nx, Ny, Nz = grid_shape
    x = np.linspace(points[:,0].min(), points[:,0].max(), Nx)
    y = np.linspace(points[:,1].min(), points[:,1].max(), Ny)
    z = np.linspace(points[:,2].min(), points[:,2].max(), Nz)
    grid_x, grid_y, grid_z = np.meshgrid(x, y, z, indexing="ij")

    grid_points = np.column_stack([grid_x.ravel(), grid_y.ravel(), grid_z.ravel()])

    # GP predictions
    mean, std = gp.predict(grid_points, return_std=True)

    # Reshape into 3D
    mean_grid = mean.reshape(grid_shape)
    std_grid = std.reshape(grid_shape)

    return grid_x, grid_y, grid_z, mean_grid, std_grid

# Parse command line arguments
def parse_cli():
        dims = int(sys.argv[1]) # dimension
        N = int(sys.argv[2]) # N = array size, i.e size of each dimension
        Q = int(sys.argv[3]) # Q = number of queries 
        return dims, N, Q

# Pick random points within the dimension
def pick_points(N, Q):
    points = np.random.randint(0, N, (Q, 3)) #min = 0, max = N, size = (Q,3)
    return points

# Input queries into titan and record answers
def submit_queries(points):
    values = []

    for i in range(len(points)):
        print(points[i][0], ",", points[i][1], ",", points[i][2], flush=True)
        line = sys.stdin.readline()
        values.append(float(line.strip()))

    return values

def avg(points, values, N):

    list_average = sum(values) / len(values)
    #array_average = np.mean(values)
    #print (array_average)

    SS_length = N*N*N

    state_space = [list_average] * SS_length

    return state_space


def main():

    dims, N, Q = parse_cli()
    #print(dims)
    #print(N)
    #print(Q)
    #dims = 3
    #N = 3
    #Q = 5


    points = pick_points(N, Q)
    #print(points)

    values = submit_queries(points)
    #print(values)

    state = avg(points,values, N)

    grid_x, grid_y, grid_z = gp_3d_reconstruction(points, values, grid_shape=(30, 30, 30))

    # Print final state
    for i in range(len(state)):
        print(state[i], end = ' ')
   
   # Flush output
    write = sys.stdout.write
    write("\n")
    sys.stdout.flush()

main()