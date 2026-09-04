# Python 只有單行註解  115.07.21 練習 01 basic data type
# 數值(整數，浮點數)

a = 10          # 整數
print(type(a))  # type：查詢資料型態
print(id(a))    # id：查詢記憶體位置
b = 12.3        # 浮點數
print(type(b))
print(id(b))

# boolean (Ture,False) 
a = True 

c = 10
print(type(c))
print(id(c))

# Python的多行註解要用字串(string)來表示，且用單引號和雙引號都沒差。
s = 'hello'
s1 = "hello"
s2 = '''
# 三個單引號或雙引號之間的區域，都可以當作註解
# 第2列
# 第3列
'''
s3 = """
# 三個單引號或雙引號之間的區域，都可以當作註解
# 第2列
# 第3列
"""

'''
這是一個多行字串
可以用來當作
長篇的程式碼註解
'''
print("哈囉，世界")

print(s,s1,s2,s3)
# Python變數命名規則：
# 1.開頭只能是英文或底線(開頭不能是數字)
# 2.不能有空格(若有第二個單字以上要用底線分隔，例如：my_name)
# 3.不能有特殊符號(底線除外)
# 4.區分大小寫(建議都用小寫)
# 5.不能是關鍵字
# 6.盡量使用有意義的名稱
# 例如： # a = 1 ，b = 3.14，name = 'jack' ，is_student = True (True,False開頭要用大寫)

# container(容器)：用來放多項資料的盒子，Python的容器資料型態如下：
# (1) tuple(元組)，不可變，用小括號()表示，元素不重複，主要用於順序型資料
# (2) list(串列)，可變，用中括號[]表示，元素可重複
# (3) dict(字典)，鍵值對，用大括號{}表示，鍵不可重複，值可重複
# (4) set(集合)，不可重複，用大括號{}表示，無順序性
# 其他語言的 array/vector 陣列(資料須為相同類型)，Python的 list(串列)不限資料類型

# Tuple(元組)的練習：
t1 = () # 空的tuple
t2 = (1,2,3) #  三個整數的tuple
t3 = 'apple','banana','cherry' # 逗號分隔，自動轉成 tuple
t4 = (1,) # 只有一個元素的tupl ，逗號不可省略
t5 = (1,'apple',True) # 混合資料型態的tuple

print(type(t1),type(t2),type(t3),type(t4),type(t5)) 

# 讀取Tuple中的某一個值，透過index(索引)來讀取。
print(t2[1]) # 讀取第二個元素
# 修正tuple中的每一個值，透過t2.()

# List: 串列 [ ]
l1 = [] # 空的 list
print(l1)
l2 = [1,2,3]
print(l2)
l3 = [1,2,3,4]
print(l3)
l4 = [1,'apple',True] # 混合資料型態的 list
print(l4)




# dictionary: 字典 {key:value}
fruits = {'apple':10,'banana':50,'cherry':8}
# 讀取 dictionary 中的某一個值，透過key(鍵)來讀取。
print(fruits["apple"])
# 修正 dictionary 中的某一個值，透過key(鍵)來修改。
fruits['apple'] = 13
print(fruits["apple"])

