# 거스름돈

money = int(input())

result_money = 1000 - money
count = 0

if result_money // 500 >= 1 :
    count += result_money // 500
    result_money = result_money % 500

if result_money // 100 >= 1 :
    count += result_money // 100
    result_money = result_money % 100

if result_money // 50 >= 1 :
    count += result_money // 50
    result_money = result_money % 50

if result_money // 10 >= 1 :
    count += result_money // 10
    result_money = result_money % 10

if result_money // 5 >= 1 :
    count += result_money // 5
    result_money = result_money % 5

if result_money // 1 >= 1 :
    count += result_money // 1
    result_money = result_money % 1

print(count)


