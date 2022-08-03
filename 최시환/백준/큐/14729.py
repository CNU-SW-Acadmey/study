# 칠무해

import sys

num = int(input())
ls = []
for i in range(num):
    n = float(sys.stdin.readline())
    ls.append(n)

ls.sort()

for i in range(7):
    print(f"{ls[i]:.3f}")



