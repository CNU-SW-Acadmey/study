# 큐

import sys

ls = []

num = int(input())

for i in range(num):
    string = list(sys.stdin.readline().split())
    
    if string[0] == 'push':
        ls.append(string[1])
        continue
    elif string[0] == 'pop':
        if len(ls) == 0:
            print(-1)
            continue
        print(ls.pop(0))
    elif string[0] == 'size':
        print(len(ls))
        continue
    elif string[0] == 'empty':
        if len(ls) == 0:
            print(1)
        else:
            print(0)
        continue    
    elif string[0] == 'front':
        if len(ls) == 0:
            print(-1)
            continue
        print(ls[0])
    elif string[0] == 'back':
        if len(ls) == 0:
            print(-1)
            continue
        print(ls[-1])


