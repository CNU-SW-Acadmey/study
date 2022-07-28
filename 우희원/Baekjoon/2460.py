# 지능형 기차2

m = 0
n = 0
for _ in range(10) :
    a, b = map(int, input().split())
    m -= a
    m += b
    n = max(m, n)
print(n)

# heewon 브랜치에서 수정