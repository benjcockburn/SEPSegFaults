#!/usr/bin/env python3

d, n, q = map(int, input().split())

for _ in range(q):
    if d == 1:
        print(0, flush=True)
    elif d == 2:
        print("0,0", flush=True)
    else:
        print("0,0,0", flush=True)
    try:
        input()
    except EOFError:
        break

if d == 1:
    print(" ".join(["0"] * n), flush=True)
elif d == 2:
    for _ in range(n):
        print(" ".join(["0"] * n), flush=True)
else:
    for _ in range(n):
        for _ in range(n):
            print(" ".join(["0"] * n), flush=True)
