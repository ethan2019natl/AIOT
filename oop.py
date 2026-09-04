# 字串的格式化表示法
# 1. %
from copy import copy
name = "peter"
s = "hello, %s !" % name
print(s)

# 多個變數
age = 10
s1 = "%s is %d years old." % (name, age)
print(s1)

# 針對數值(int, float)的格式定義
s2 = "ID: %05d" % 42
print(s2)
s2 = "ID: %5d" % 42 # 預設向右對齊
print(s2)
s2 = "ID: %-5d" % 42 # 向左對齊
print(s2)

# 字典
data = {"name": "peter", "score": 80}
s3 = "%(name)s's score  is %(score)d." % data
print(s3)

# 2. {}
# 按順序
s4 = "{} is {} years old.".format(name, age)
print(s4)
# index: 可重複存取, 也沒有所謂的順序性
s4 = "{0} is {1} years old. {0} is very cute.".format(name, age)
print(s4)
# key: 可重複存取, 也沒有所謂的順序性
print("{name}'s score  is {score}.".format(score=85, name="peter"))

# 針對數值(int, float)的格式定義
print("ID: {:05d}".format(42))
print("ID: {:0>5d}".format(42))
print("ID: {:<5d}".format(42))
print("ID: {:>10.3f}".format(3.1415926))

# f-string: {變數}
print(f"{name} is {age} years old. {name} is very cute.")
num = 42
print(f"ID: {num:05d}")
print(f"ID: {num:0>5d}")
print(f"ID: {num:<5d}")
print(f"ID: {3.1415926:>10.3f}")

# \:跳脫符號
print("hello,\n world!")
print("hello,\\n world!")

# r-string
print("hello,\n world!")
print(r"hello,\n world!")

# 字串的運算: +, *
# 字串的串接
# +:
s1 = 'hello'
s2 = ' wold!'
s = s1 + s2
print(s)

# *:
s1 = "*"
print(s1*60)

# slicing: [start(包含): stop(不包含): step(取值的規則)]
s = "hello world"
s1 = s[1:9:2]
print(s1)
s1 = s[-10:-2:2]
print(s1)

# 反向取值: 由step +/- 符號控制
s2 = s[7:0:-2]
print(s2)

# 把原始資料做inverse
s3 = s[-1::-1]
print(s3)

# 全部取值
s4 = s[::]
print(s4)

# string oop
# 轉大寫
s = "hello world"
s1 = s.upper()
print(f"s1:{s1}")
s2 = s1.capitalize()
print(f"s2:{s2}")
s3 = s2.swapcase()
print(f"s3:{s3}")

# split:拆解字串 
l1 = s.split(' ')
print(l1)
l1 = s.split('o')
print(l1)

# replace: 替換
s1 = s.replace('l', '--')
print(f"s1:{s1}")

# strip: 移除字串頭尾的空白符號
s = "   hello, world "
s1 = s.strip()
print(f"s1:{s1}")

# 搜尋子字串/關鍵字
s = "qwertydfghj456789wert456fghwr"
s1 = s.find('we')
print(f"s1:{s1}") # 找到第一組符合條件的子字串位置
s1 = s.find('123')
print(f"s1:{s1}") # 找不到符合條件的子字串: -1


# list oop
# 加法運算: 串列結合
l1 = [1,2,3]
l2 = [4,5,6]
l = l1 + l2
print(f"l:{l}")

# 新增多個串列資料的方法
l1.extend(l2)
print(f"l1:{l1}")

# 新增一個串列資料的方法: 從尾巴開始加入新資料
l1.append(10)
print(f"l1:{l1}")
l1.append(l2)
print(f"l1:{l1}")

# slicing
l1 = [1,2,3,4,5,6,7,8,9,10]
l2 = l1[::2]
print(f"l2{l2}")

# 使用slicing 插入並取代原始資料
l1[2:5] = "hello"
print(f"l1:{l1}")

# insert: 插入
l1.insert(0, "world")
print(f"l1: {l1}")

# pop: 刪除元素
removed_data = l1.pop()
print(f"l1: {l1}")
print(f"removed_data: {removed_data}")
# 指定刪除資料所在位置
removed_data = l1.pop(5)
print(f"l1: {l1}")
print(f"removed_data: {removed_data}")

# clear(): 刪除串列中的所有元素
l1.clear()
print(f"l1: {l1}")

# sort: 排序, 預設升冪排序(小到大)
l1 = [54, 3, 36, 78, 100, 10]
l1.sort()
print(f"l1: {l1}")
# 先作升冪後, 再做降冪
l2 = l1[::-1]
print(f"l2: {l2}")

# 降冪排序
l1 = [54, 3, 36, 78, 100, 10]
l1.sort(reverse=True)
print(f"l1: {l1}")

# count: 計算元素出現的次數
l1 = [1,2,2,3,3,3,4,5,5]
num = l1.count(2)
print(f"num 2 : {num}")

# in: 檢查指定元素有沒有存在
print(5 in l1)
print(7 in l1)
print(7 not in l1)

# join: 把串列中的字串元素透過指定的符號串接起來, 變成string
l1 = ['apple', 'banana','orange']
s = '_'.join(l1)
print(f"s: {s}")

s = "hello, world! How are you?"
l1 = s.split(' ')
s1 = '_'.join(l1)
print(f"s1: {s1}")

# 計算串列中有多少個元素
print(f"l1: {len(l1)}")
print(f"s: {len(s)}")

# 多重給值
ch, en, math = [50, 60, 70]
print(f"ch: {ch}")
print(f"math: {math}")

# 部分拆解: * (打包)
l1 = [1,2,3,4,5,6]
first, *middle, last = l1
print(f"first: {first}")
print(f"middle: {middle}")
print(f"last: {last}")

# _: 是一種佔位符, 但是他代表不重要的資訊
ch, _, math = [50, 60, 70]
print(f"ch: {ch}")
print(f"math: {math}")

l1 = [1,2,3,4,5,6]
*_, last2, last1 = l1
print(f"last2: {last2}")
print(f"last1: {last1}")


# 複製
l1 = [1,2,3,4,5,6]
l2 = l1
l3 = l1[::]
l4 = l1.copy()
print(f"l1: {l1}")
print(f"l2: {l2}")
print(f"l3: {l3}")
print(f"l4: {l4}")
print('-'*30)
l2[0] = 10
print(f"l1: {l1}")
print(f"l2: {l2}")
print(f"l3: {l3}")
print(f"l4: {l4}")
print('-'*30)
print(f"l1 id: {id(l1)}")
print(f"l2 id: {id(l2)}")
print(f"l3 id: {id(l3)}")
print(f"l4 id: {id(l4)}")
print('-'*30)

print(f"l1[1] id: {id(l1[1])}")
print(f"l2[1] id: {id(l2[1])}")
print(f"l3[1] id: {id(l3[1])}")
print(f"l4[1] id: {id(l4[1])}")
print('-'*30)

l1 = [1,2,3,4,5,6,[10,11,12]]
l2 = l1
l3 = l1[::]
l4 = l1.copy()

import copy
l5 = copy.deepcopy(l1)

print(f"l1: {l1}")
print(f"l2: {l2}")
print(f"l3: {l3}")
print(f"l4: {l4}")
print(f"l5: {l5}")
print('-'*30)

l2[0] = 10
print(f"l1: {l1}")
print(f"l2: {l2}")
print(f"l3: {l3}")
print(f"l4: {l4}")
print(f"l5: {l5}")
print('-'*30)

l1[-1][1] = 110
print(f"l1: {l1}")
print(f"l2: {l2}")
print(f"l3: {l3}")
print(f"l4: {l4}")
print(f"l5: {l5}")
print('-'*30)

# tuple
t1 = (1,2,3)
t2 = (4,)
t3 = t1 + t2
print(f"t3: {t3}")

tl = list(t1)
tl[0] = 10
t1 = tuple(tl)
print(f"t1: {t1}")

# count: 計算元素出現次數
t1 = (1,2,2,3,3,3,4,5,5)
num = t1.count(2)
print(f"num 2 : {num}")

# index: 找出第一個符合特定元素所在index位置
ind = t1.index(3)
print(f"ind 3 : {ind}")

ind = t1.index(3, ind+1)
print(f"ind 3 : {ind}")

# error
# ind = t1.index(6, ind+1)
# print(f"ind 3 : {ind}")

# swap: tuple + unpack
a = 10
b = 20
print(f"b: {b}")
print(f"a: {a}")
b, a = a, b
print(f"b: {b}")
print(f"a: {a}")

# 部分拆解: * (打包)
l1 = (1,2,3,4,5,6)
first, *middle, last = l1
print(f"first: {first}")
print(f"middle: {middle}")
print(f"last: {last}")

# _: 是一種佔位符, 但是他代表不重要的資訊
ch, _, math = (50, 60, 70)
print(f"ch: {ch}")
print(f"math: {math}")

l1 = (1,2,3,4,5,6)
*_, last2, last1 = l1
print(f"last2: {last2}")
print(f"last1: {last1}")


# dictionary
d = {"name": "peter", "age":20, "email": "123@sdf"}
# 讀取資料
print(d['name'])
print(d.get('name'))
# 新增資料
d['phone'] = "1234567890"
d.setdefault('blood', 'B')
print(d)

# 移除
del d['blood']
print(d)

# 新增多筆資料
d1 = {"height": 160, "weight": 65}
d.update(d1)
print(d)

d2 = {**d, **d1}
print(d2)

d["height"] = 200
d3 = d1 | d | d2 # 以前面出現為優先
print(f"d3: {d3}")

# 取所有的鍵值
print(d.keys())

# 取所有的值
print(d.values())

print(list(d.items()))