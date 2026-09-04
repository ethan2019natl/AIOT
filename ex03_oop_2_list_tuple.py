# 115.08.03 練習 oop (物件導向程式設計)
# 物件功能的操作-list-串列-tuple-元組


# List 串列的OOP
# 和string一樣有加法運算：串列結合

l1 = [1,2,3]
l2 = [4,5,6]
l = l1 + l2
print(f"l: {l}")


# append(): 新增一個資料的方法
l1.append(10)  
print(f"l1: {l1}") 

l1.append(12)  
print(f"l1: {l1}")   #注意也可以一直累加到後面


# extend(): 新增多個串列資料的方法
l1.extend(l2)  # extend()擴增(原本的list會改變)；可以將多個元素加到原本的list中
print(f"l1: {l1}")


# slicing

l1 = [1,2,3,4,5,6,7,8,9,10]
l2 = l1[::2] # 取奇數，從index=0開始，間隔2個取1個
print(l2)
l3 = l1[1::2] # 取偶數，從index=1開始，間隔2個取1個
print(l3)

# 使用slicing 取代原始資料
l1[2:5] = "hello"  # 切片取資料，可以將多個元素加到原本的list中
print(f"l1: {l1}") # 注意! 清單的長度會改變!

l1 = [1,2,3,4,5,6,7,8,9,10]
l1[2:5] = ["hello"]  # 比較加上[]的狀況，清單的長度會改變!
print(f"l1: {l1}")

# insert(): 插入資料(可指定位置索引值)
l1 = [1,2,3,4,5,6,7,8,9,10]
l1.insert(0,"world")
print(f"l1: {l1}")

# pop: 刪除元素
removed_data = l1.pop()
print(f"l1: {l1}")
print(f"removed_data: {removed_data}")
# 指定刪除資料所在位置
removed_data = l1.pop(5)
print(f"l1: {l1}")
print(f"removed_data: {removed_data}")

# clear(): 清空串列中所有元素，但變數依然存在
l1.clear() 
print(f"l1: {l1}")

# sort(): 排序，預設升冪(由小到大)，會改變原本的list
l1 = [53,3,36,78,100,10]
l1.sort() 
print(f"l1: {l1}")

l2 = l1[::-1]  #先做升冪，之後再做降冪，可以用這招(但前提原本的l1要是升冪)
print(f"l2: {l2}")


l1.sort(reverse=True) # 降冪(由大到小)，會改變原本的list
print(f"l1: {l1}")  


# sorted(): 排序，預設升冪(由小到大)，不會改變原本的list，會回覆一個新的list
l1 = [53,3,36,78,100,10]
l2 = sorted(l1)
print(f"l2: {l2}")

l3 = sorted(l1,reverse=True)
print(f"l3: {l3}")

# count: 計算指定元素出現的次數(符合條件的數量)
l1 = [1,1,1,2,2,3,4,4,5]
print(f"l1 num(2)出現次數: {l1.count(1)}")


# in: 檢查指定元素有沒有存在
print(5 in l1)
print(7 in l1)
print(7 not in l1)


# join ：把串列中的元素，透過指定的符號(字串)，組合成一個字串(原本的list不會改變)
l1 = ['apple','banana','orange']
s1= '_'.join(l1)  #以下底線當作分隔符，將串列中的元素組合成一個字串
print(f"s1: {s1}") 

s = "Hello,World! How are you?"
l1 = s.split(' ') # 用空格當作分隔符，將字串切成 list
s1= '_'.join(l1)  #以下底線當作分隔符，將串列中的元素組合成一個字串
print(f"s1: {s1}") 

# 計算串列中有元素的總數
l1 = [1,2,3,4,5]
s = "Hello,World! How are you?"
print(f"l1: {len(l1)}") # 計算串列中有多少個元素
print(f"s: {len(s)}") # 計算字串中有多少個字(包含空白)

# 多重給值 (拆解 list)
ch, en, math = [50,60,70]
print(f"ch: {ch}")
print(f"en: {en}")
print(f"math: {math}")

# 部分拆解： * (打包)
l1 = [1,2,3,4,5,6]
first,*middle,last = l1
print(f"first: {first}")
print(f"middle: {middle}")
print(f"last: {last}")

# _: 當作不需要的變數，是一種佔位符號，可以避免報錯，但也會浪費記憶體
ch, _, math = [50, 60, 70]
print(f"ch: {ch}")
print(f"math: {math}")

l1 = [1,2,3,4,5]
# _ 當作變數名稱，可以避免報錯，但也會浪費記憶體
*_, last2, last1 = l1
print(f"last2: {last2}")
print(f"last1: {last1}")

# 複製
l1 = [1,2,3,4,5,[10,11,12]] #內層串列為巢狀結構
l2 = l1 * 2  # 串列的重複
l3 = l1[::]
l4 = l1.copy()
import copy
l5 = copy.deepcopy(l1)

print(f"l1: {l1}")
print(f"l2: {l2}")
print(f"l3: {l3}")
print(f"l4: {l4}")
print("-"*30)

l2[0] = 10  # 修改 l2 第 1 個元素為 10
print(f"l1: {l1}")
print(f"l2: {l2}") 
print(f"l3: {l3}")
print(f"l4: {l4}")
print("-"*30)

l1[-1][1] = 110
print(f"l1: {l1}")
print(f"l2: {l2}") 
print(f"l3: {l3}")
print(f"l4: {l4}")
print(f"l5: {l5}")
print("-"*30)


print(f"l1 id: {id(l1)}")
print(f"l2 id: {id(l2)}")
print(f"l3 id: {id(l3)}")
print(f"l4 id: {id(l4)}")
print("-"*30)

print(f"l1 id: {id(l1[1])}")
print(f"l2 id: {id(l2[1])}")
print(f"l3 id: {id(l3[1])}")
print(f"l4 id: {id(l4[1])}")
print("-"*30)


# tuple : 元組 (裡面的資料無法修改) -> 記得中間要加逗號
t1 = (1,2,3)
t2 = (4,)
t3 = t1 +t2
print(f"t2: {t3}")

tl = list(t1)
tl[0] = 10
t1 = tuple(tl)
print(f"t1: {t1}")

# count： 計算指定元素出現的次數(符合條件的數量)
t1 = (1,1,1,2,2,3,4,4,5)
print(f"t1 num(1)出現次數: {t1.count(1)}")

# index: 找到指定元素第一次出現的索引值
ind = t1.index(3)
print(f"t1 num(3)第一次出現的索引值: {ind}")

# error
# ind = t1.index(3,ind+1)  # 從ind+1的位置開始找，往後找(不會找前面)
# print(f"t1 num(3)下一個出現的索引值: {ind}")  # 因為只找到一個，所以會出現錯誤訊息


# swap 交换 (x,y) = (y,x)  利用tuple的特性，直接將元素進行交換
a = 10
b = 20
print(f"交換前 a: {a} b: {b}")
(a,b) = (b,a)
print(f"交換後a: {a}")
print(f"交換後b: {b}")

