# if 條件
score = 59
if score >= 60:
    print("及格")
else:
    print("不及格")


# 巢狀 if 條件:
day = "周末"
weather = "晴天"
if day == "周末":
    if weather == "晴天":
        print("出門散步")
    else:
        print("在家看電視")
else:
    print("取工作")

# if... elif...else (具優先權)
milk = "初鹿"
if milk == "瑞穗":
    print("買3瓶")
elif milk == "小農":
    print("買2瓶")
elif milk == "初鹿":
    print("買1瓶")
else:
    print("不買")


# pass: 為定義的區塊, 可用pass取代
if score:
    pass
else:
    pass

print(list(range(10)))

# for迴圈
# 1. 固定次數: for in range()
for i in range(10):
    print(f"i: {i}")


# 2. 不提供次數: for in container
l1 = [1,2,3,4,5,6]
for element in l1:
    print(f"element: {element}")

d = {"name": "peter", "age": 20, "email": "123@jl"}
for key in d:
    print(f"key: {key}")

for value in d.values():
    print(f"value: {value}")


for t in d.items():
    print(f"key: {t[0]}, value: {t[1]}")

for key, value in d.items():
    print(f"key: {key}, value: {value}")

print(list(enumerate(l1)))
# tuple, list: enumerate
for indx, value   in enumerate(l1):
    print(f"key: {indx}, value: {value}")


# 控制迴圈行為: break, continue
for i in range(10):
    if i == 5:
        continue #bypass底下定義的所有行為
    print(f"i: {i}")


for i in range(10):
    if i == 5:
        break #bypass底下定義的所有行為 + 迴圈終止
    print(f"i: {i}")

# 內積運算
a = [1,2,3]
b = [4,5,6]
sum = 0
for a_v, b_v in zip(a,b):
    sum += a_v * b_v

print(f"a*b內積 = {sum}")

# while
i = 0
while i<10:
    print(f"i: {i}")
    i = i + 1


# try...except:
try:
    x = 1/0
except ZeroDivisionError as error:
    print(f"error msg: {error}")


# 串列生成式
l1 = [i for i in range(10)]
print(f"l1: {l1}")

l2 = []
for i in range(10):
    l2.append(i)
print(f"l2: {l2}")

l1 = [i*10 for i in range(10)]
print(f"l1: {l1}")

l1 = [i for i in range(10) if i%2==0]
print(f"l1: {l1}")

# 矩陣相乘
M1 = [[1,2],[3,4]]
M2 = [[5,6],[7,8]]

r = [[M1[i][j] * M2[i][j] for j in range(len(M1[0]))] for i in range(len(M1))]
print(r)


t = ()
for i in range(10):
    t = t + (i,)

print(f"t: {t}")