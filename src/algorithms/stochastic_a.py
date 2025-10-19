import sys

def parse_cli():
    dims = int(sys.argv[1])
    N = int(sys.argv[2])
    Q = int(sys.argv[3])
    return dims, N, Q

def query_point(x, y, max_queries, query_counter):
    """Query the same point twice and return a probability prediction."""
    results = []
    for _ in range(2):
        if query_counter[0] >= max_queries:
            print(f"Reached max queries ({max_queries})", file=sys.stderr)
            break  # Do not exceed Q
        try:
            print(f"{x},{y}", flush=True)  # Must be exactly x,y
            line = sys.stdin.readline()
            if not line:
                raise RuntimeError(f"No input received for query ({x},{y})")
            val = int(line.strip())
            if val not in [0, 1]:
                raise ValueError(f"Invalid input {val} at ({x},{y})")
            results.append(val)
            query_counter[0] += 1
        except Exception as e:
            print(f"Error reading query ({x},{y}): {e}", file=sys.stderr)
            results.append(0)  # fallback to 0

    # Map results to probability
    total = sum(results)
    return {0: 0.1, 1: 0.5, 2: 0.9}.get(total, 0.5)  # fallback 0.5

def main():
    dims, N, Q = parse_cli()
    if dims != 2:
        print("This version handles 2D only.", file=sys.stderr)
        return

    predictions = [[0.0 for j in range(N)] for i in range(N)]
    query_counter = [0]  # Use a list to make it mutable inside functions

    for i in range(N):
        for j in range(N):
            predictions[i][j] = query_point(i, j, Q, query_counter)

    # Print the 2D prediction matrix
    for i in range(N):
        print(" ".join(f"{predictions[i][j]:.3f}" for j in range(N)))

if __name__ == "__main__":
    main()