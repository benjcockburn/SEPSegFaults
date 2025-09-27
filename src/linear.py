import sys
# import math

# Parse command line arguments
def parse_cli():
        dims = int(sys.argv[1])
        N = int(sys.argv[2])
        Q = int(sys.argv[3])
        return dims, N, Q

# Pick evenly distributed query points in dim == 1
def pick_points(N, Q):
    min = 0
    max = N - 1
    result = [0] * Q
    iterator = 0
    
    for i in range(Q-1):
        # print("i = ", i)
        temp = min + i * ( (max - min) / (Q - 1))
        # print("Temp", temp)
        result[i] = round(temp)
        # print("Result", result[i])
        iterator += 1

    result[iterator] = max
    # print("Result before shuffle", result)
    return result

# Input queries into titan and record answers
def submit_queries(queries):
    answer = []

    for i in range(len(queries)):
        print(queries[i], flush=True)
        line = sys.stdin.readline()
        answer.append(float(line.strip()))

    return answer

# Linear interpolation algorithm to generate state space
def interp(y_known, x_known, N):

    x_query = list(range(0, N+1))
    y_interp = []

    for x in x_query:
        # If x is exactly known, just use it
        if x in x_known:
            y_interp.append(y_known[x_known.index(x)])
        else:
            # Find the two known points surrounding x
            for i in range(len(x_known) - 1):
                if x_known[i] < x < x_known[i + 1]:
                    x0, x1 = x_known[i], x_known[i + 1]
                    y0, y1 = y_known[i], y_known[i + 1]

                    # Linear interpolation formula
                    y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                    y_interp.append(float(y))
                    break

    return y_interp

def main():

    dims, N, Q = parse_cli()
    # dims = 1
    # N = 10
    # Q = 5


    queries = pick_points(N, Q)
    # print(queries)

    answer = submit_queries(queries)
    # print(answer)

    state = interp(answer,queries, N)

    # Print final state
    for i in range(len(state)):
        print(state[i], end = ' ')
   
   # Flush output
    write = sys.stdout.write
    write("\n")
    sys.stdout.flush()

main()