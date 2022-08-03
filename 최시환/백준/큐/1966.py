# 프린터 큐

from collections import deque


num = int(input())

for i in range(num):
    count = 0
    ls = deque()
    lst = list(map(int , input().split()))
    n = lst[0]
    m = lst[1]

    num_lst = list(map(int , input().split()))
    for i in range(len(num_lst)):
        if i == m:
            ls.append([num_lst[i] , 'true'])
        else:
            ls.append([num_lst[i] , 'false'])
    
    while(len(ls) > 1):
        if list(ls)[0][0] >= max(list(ls)[1:] , key = lambda x : x[0])[0]:
            a = ls.popleft()
            if a[1] == 'true':
              break
            count += 1
        else:
            a = ls.popleft()
            ls.append(a)

    print(count+1)
    
        
        

        
