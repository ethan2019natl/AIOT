
# 練習04 常見運算子 (Operator) 優先順序為：算數 > 比較 > 邏輯

# 算數運算子 (+, -, *, /, //, %, **)
a = 2
b = 2
a + b  #加
a - b  #減
a * b  #乘
a / b  #除
a // b #整數除
a % b  #取餘數
a ** b #平方

# 補充技巧：滑鼠游標點選在同類型文字出現反白時，可以用滑鼠中鍵壓著不放來拉動，一次替換所選中的內容

# 比較運算子 (==、<、>、<=、>=、!=) 結果傳回布林值 True/False
print(a == b)   #a是否等於b True/False
print(a<b)      #a是否小於b True/False
print(a>b)      #a是否大於b True/False
print(a<=b)     #a是否小於等於b True/False
print(a>=b)     #a是否大於等於b True/False
print(a!=b)     #a是否不等於b True/False

# 邏輯運算子 (and、or、not) 結果傳回布林值 True/False
# 補充：用條件一(and/or/not)和條件二、條件三.....組成的條件判斷，結果傳回布林值 True/False

print(True and False)
print(True and True)
print(False and False)
print(True or False)
print(False or False)
print(not True)
print(not False)

a = True
b = False
print(a and b)  #a and b
print(a or b)   #a or b
print(not a)    #not a

# assign: =
a = 5
a += 2  # a = a + 2  簡寫
a -= 2  # a = a - 2  簡寫
a *= 2  # a = a * 2  簡寫
a /= 2  # a = a / 2  簡寫
a //= 2 # a = a // 2 簡寫
a %= 2  # a = a % 2  簡寫
a **= 2 # a = a ** 2 簡寫


# in: 成員運算子 (在...之內)  not  in: 不在...之內
# is: 身分運算子 (比較記憶體位址是否相同)   is not: 

a = [1,2,3]
b = a
c = a.copy()

print(a in [1,2,3]) #True (在...之內)
print(a not in [1,2,3]) #False (不在...之內)
print(a is b)   #True (記憶體位址相同)
print(a is c)   #False (記憶體位址不同)  
print(a == c)   #True (內容相同)
print(a is not b) #False (記憶體位址相同)
print(a is not c) #True (記憶體位址不同)


