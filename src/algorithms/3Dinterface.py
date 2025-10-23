import sys
import numpy as np
# import math

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

    # Print final state
    for i in range(len(state)):
        print(state[i], end = ' ')
   
   # Flush output
    write = sys.stdout.write
    write("\n")
    sys.stdout.flush()

main()