# basic data type
# 數值(整數, 浮點數)
a = 10
# type: 查詢資料型態
print(type(a))
# id: 查詢物件(10,12.3,True,...)所在記憶體位置
print(id(a))
b = 12.3
print(type(b))
print(id(b))

# boolean(True, False)
a = True
print(type(a))
print(id(a))
c = 10
print(type(c))
print(id(c))

# 字串 String
s = 'hello'
s1 = "a"
s2 = '''
gkj;
    sdfk;l
 '''
s3 = """
asdjkl
  sdf8746
  """
print(s, s1, s2, s3)

# Tuple 元組
t1 = () # 空 tuple
t2 = (1, 2, 3)
t3 = 'a', 'b', 'c' # 逗號分隔，自動轉成 tuple
t4 = 1, # 單元素 tuple 必須加逗號， otherwise is int
t5 = (1, 12.3, "hi", False)
print(type(t1), type(t2), type(t3), type(t4))

# 讀取tuple中的某一個值: 透過 [ index ]
print(t2[1]) # 2
# 修正tuple中的某一個值: 透過 [ index ]
# t2[1] = 20 # error:違反了不可變性

# List: 串列 []
l1 = []
l2 = [1, 2, 3]
l3 = ['a', 'b', 'c']
l4 = [1, 'a', True, 12.3]
print(type(l1), type(l2), type(l3), type(l4))

# 讀取list中的某一個值: 透過 [ index ]
print(l2[1]) # 2
# 修正list中的某一個值: 透過 [ index ]
l2[1] = 20 
print(l2)

# dictionary : 字典 {key: value}
fruits = {"apple": 10, "banana":50, "orange": 8}
# 讀取dictionary中的某一個值: 透過 [ key ]
print(fruits["orange"]) # 8
# 修正dictionary中的某一個值: 透過 [ key ]
fruits["orange"] = 13
print(fruits["orange"])

# 2D
scores = [{"國文": 90, "英文": 80, "數學":60},
            {"國文": 40, "英文": 90, "數學":80},
            {"國文": 50, "英文": 100, "數學":90},
            {"國文": 60, "英文": 30, "數學":70},
            {"國文": 70, "英文": 20, "數學":60},
            ]
# read 2D scores[第幾位學生][科目]
print(scores[0]["國文"])


# 資料型態轉換
# int(), float(), str()
data = 10
print(float(data))
print(type(str(data)))

data = '123'
print(int(data))
print(float(data))