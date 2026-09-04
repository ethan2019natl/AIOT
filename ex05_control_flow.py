# 條件判斷 (if 條件)

score = 59
if score >= 60 :
    print("及格")
else :
    print("不及格") 


# 巢狀判斷 (if 巢狀)
day = '周末'
weather = '晴天'
if day == '周末' :
    if weather == '晴天' :
        print("出門散步")
    else :
        print("在家看電視")
else :
    print("去上班工作")

# 若想要先定義框架，之後再決定內容，可用 pass 來佔位作預留 (pass 也可以用在def等區塊內，代表目前不做任何事)

milk = '初鹿'
if milk == '瑞穗':
    print("買3瓶")
elif milk == '光泉':
    print("買2瓶")
elif milk == '初鹿':
    print("買1瓶")
else:
    print("都不買") 


if score:
    pass
    print("注意pass之後還是會執行") # 注意在if判斷中，pass後面的程式碼也會被執行
else:
    pass


# range 函式

print(list(range(10)))    # 輸出 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# for 迴圈
# 1. 直接輸入數值範圍： for i in range(s1,s2,s3)  s1: 開始數  s2: 結束數(不包含)  s3: 間距

for i in range(10):
    print(f"i:{i}")  # range 從0開始數，所以會跑0~9，共10次

for i in range(5,10):
    print(f"i:{i}") # range 從5開始數，所以會跑5~9，共5次

for i in range(2,10,2):
    print(f"i:{i}") # range 從2開始數，所以會跑2~9，間距2

# 2. 使用變數定義次數： for in container (容器)

l1 = [1,2,3,4,5,6]
for element in l1:
    print(f"elemeny:{element}")

d = {'name':'pater','age':20,'email':'peter@mail'}
for key in d:
    print(f"key:{key}")

for value in d.values():
    print(f"value:{value}")


# items() 的應用 (將 key 與 value 一次取出的方法，注意以下兩種方法結果相同)

for t in d.items():  # 先將key與value組合成元組
    print(f"key:{t[0]},value:{t[1]}")


for key,value in d.items():     # 最常用的寫法，直接將元組拆解成變數 (unpacking拆包)
    print(f"key:{key},value:{value}")


# tuple, list, enumerate 的應用
# for i in enumerate(l1) 將一個可迭代的對象（如列表、元組或字串）轉換為索引序列後輸出

for index, value in enumerate(l1):
    print(f"index:{index},value:{value}")


# 控制迴圈行為： break, continue
# 1.break 直接跳出迴圈    

for i in range(10):
    if i == 5:
        break  # i等於5時,直接跳出迴圈
    print(f"i: {i}")
   

# 2.continue 跳過當前迴圈的剩餘程式碼，並立即進入下一輪迴圈。
# 常用於 for 和 while 迴圈中，當符合特定條件時不執行後續動作。
for i in range(10):
    if i == 5:
        continue  # i等於5時,不執行後面的程式碼,直接跳到下一次迴圈
    print(f"i: {i}") 
    
# zip() 的應用: 將多個可迭代的對象(容器)合併在一起，形成一個由元組組成的序列。
# 內積運算

a = [1,2,3]
b = [4,5,6]
sum = 0
for a_v,b_v in zip(a,b):  #zip(a, b) 會將串列轉化為 [(1, 4), (2, 5), (3, 6)] 的結構。
    sum += a_v * b_v      # sum = sum + a_v * b_v (+= 是累加運算子，將乘積加到 sum 變數中。)
print(f"a*b的內積為:{sum}")

# while 迴圈
# 1. 直接輸入數值範圍： while condition:  condition: 條件 (布林值)
i = 0
while i < 10: # 當i小於10時，迴圈會一直執行
    print(f"i: {i}")
    i = i + 1 # 每次執行後，i的值加1，通常可簡寫成 i += 1


# 2. while True (無限迴圈) 的應用:  通常會搭配 break 使用
count = 0
while True:  # 這是一個無限迴圈，條件永遠為 True，因此會一直執行，直到被 break 中斷。
    print(f"count: {count}")
    count += 1
    if count == 5:  # 設定一個中斷條件，當 count 等於 5 時，執行 break。 
        break       # 跳出迴圈，不再繼續執行。 


# try - except 的應用 
# try:  try 區塊用來包裝可能引發錯誤的程式碼。
# except ErrorType:  except 區塊用來處理特定類型的錯誤。

#try:          # 嘗試執行這行程式碼，如果發生錯誤，則跳到 except 區塊。
#    x = 1/0   # 注意此行因除數為0，會被編譯器報錯，實際應該把這行移到except下面，並搭配if來判斷除數是否為0。
#except ZeroDivisionError as error:  # ZeroDivisionError: 當程式試圖進行除以零的操作時會觸發。
#    print(f"發生錯誤 error msg:{error}")

# 串列生成式 (List Comprehension) 的應用:
# 用單行程式碼快速建立串列的方法。它的基本寫法是 [運算式 for 變數 in 可迭代物件]
# 或稱 [expression for item in iterable] ，注意 for 和 in 不可省略)
# 能取代傳統的 for 迴圈與 append 寫法，讓程式碼更簡潔易讀。

l1 = [i for i in range(10)]  
    # i 就是運算式(expression)，i會被當作元素加入列表，range(10)就是可迭代物件(iterable)，也可以寫成 [i for i in range(10)] 或 [i for i in range(10)] [i for i in range(10)]
print(f"l1:{l1}")

l2 = []  # 傳統的 for 迴圈與 append 寫法 (先定義一個空列表，然後使用 for 迴圈將元素逐一添加到列表中。)
for i in range(10):   # 注意 for 和 in 不可省略
    l2.append(i)
print(f"l2:{l2}")   

# 也可以加入運算，例如將數值乘以10
l1 = [i*10 for i in range(10)] 
print(f"l1:{l1}")

# 也可以加入條件判斷，例如只取偶數
l1 = [i for i in range(10) if i%2 == 0] # 將1到9(不包含10)中的偶數(i%2 == 0)取出並存入列表l1
print(f"l1:{l1}")

# 相當於下面 for 迴圈與 append 的寫法
l1 = [] # 傳統的 for 迴圈與 append 寫法 (先定義一個空列表，然後使用 for 迴圈將元素逐一添加到列表中。)
for i in range(10):   # 注意 for 和 in 不可省略
    if i%2 == 0:
        l1.append(i)  # 將 i 加到列表 l1 中
print(f"l1:{l1}")


# 矩陣相乘
# 建議直接使用套件進行矩陣相乘(使用 NumPy 套件，利用 @ 運算子或 np.dot() 函數)
# 以下為傳統使用for迴圈與矩陣生成式寫法：

M1 = [ [1,2], [3,4] ]
M2 = [ [5,6], [7,8] ]

r = [[M1[i][j] * M2[i][j] for j in range(len(M1[0]))]for i in range(len(M1))]
print(r)





