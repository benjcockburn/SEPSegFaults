import sys
# import math

# Parse command line arguments
def parse_cli():
        dims = int(sys.argv[1])
        N = int(sys.argv[2])
        Q = int(sys.argv[3])
        return dims, N, Q


def query_point(x,y):
    results = []

    for i in range(2):
        print(f"{x},{y}", flush=True)
        line = sys.stdin.readline().strip()
        results.append(int(line.strip()))

    if results == [1, 1]:
        return 0.9
    elif results == [0, 0]:
        return 0.1
    else:
        return 0.5


def main():
    dims, N, Q = parse_cli()

    predictions = [[0.0 for j in range(N)] for i in range(N)]

    for i in range(N):
         for j in range(N):
              predictions[i][j] = query_point(i, j)

    for i in range (N):
         print(" ".join(f"{predictions[i][j]:.1f}" for j in range(N)))
         
if __name__ == "__main__":
    main()