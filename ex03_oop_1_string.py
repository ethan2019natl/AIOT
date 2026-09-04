# 115.08.03 練習 oop (物件導向程式設計)
# 物件功能的操作-# string-字串的格式化表示法
#
# 1. %格式化表示法
# 2. format()格式化表示法
# 3. f-string格式化表示法 (建議使用)


# 第一種 %格式化表示法的單一變數
name = "peter"
s = "hello, %s !" % name
print(s)

# 第一種 %格式化表示法的兩個變數
age = 10
s1 = "%s is %d years old" % (name,age)
print(s1)

# 第一種 %格式化表示法的數值整數格式及定位方法
s2 = "ID: %05d" % 42 # 指定5位數，若數值小於五位數，自動補0
print(s2)
s2 = "ID: %5d" % 42 # 預設向右對齊
print(s2)

s2 = "ID: %-5d" % 42 # 預設向左對齊
print(s2)

# 第一種 %格式化表示法的變數使用字典方式
data = {"name":"peter","score": 80}
s3 = "%(name)s scored is %(score)d " % data
print(s3)

#第二種 format()格式化表示法，用大括弧{}當作變數的容器，用小括弧()填入變數
s4 = "{} is {} years old" .format(name,age)
print(s4)

# 改用index()指引順序，可重複存取，也沒有順序性
s4 = "{0} is {1} years old. {0} is very cute.".format(name,age)
print(s4)

# 改用key()指引順序，可重複存取，也沒有順序性
print("{name}'s score is {score}".format(name ="peter",score=80))

print("ID:{:05d}".format(42))  # 五位數，預設補0
print("ID:{:>05d}".format(42)) # 靠右對齊
print("ID:{:<05d}".format(42)) # 靠左對齊
print("ID:{:^05d}".format(42)) # 置中
print("ID:{:<10.3f}".format(3.1415926)) # 改用浮點數，10個位數，小數點後3位，靠左對齊
print("ID:{:010.3f}".format(3.1415926)) # 改用浮點數，10個位數，小數點後3位，靠右對齊，預設補0


#第三種 f-string格式化表示法，在字串前加上f，大括弧{}裡可以直接填入變數，非常直覺。
#若要對齊或改變格式，也可以在變數後面加上:加上格式符號，與format()格式化表示法相同
s4 = f"{name} is {age} years old. {name} is very cute." 
mum = 42
print(f"ID:{mum:05d}") # 五位數，預設補0  
print(f"ID:{mum:>5d}") # 靠右對齊  
print(f"ID:{mum:<5d}") # 靠左對齊  
print(f"ID:{mum:^5d}") # 置中對齊  
print(f"ID:{3.1415926:>10.3f}") # 浮點數，10個位數，小數點後3位，靠右對齊

# escape sign (跳脫/轉義符號)
print("hello,\n world!") # enter (斷行)
print("hello,\t world!") # tab (定位鍵) 
print("hello,\b world!") # backspace (退格鍵)
print("hello,\r world!") # return (游標移到開頭)
print("hello,\f world!") # form feed (換頁)
print("hello,\v world!") # vertical tab (垂直定位鍵) 
print("hello,\\ world!") # \ (反斜線) 將反斜線當成一般字元，而不是跳脫字元。
print("hello,\' world!") # ' (單引號) 將單引號成一般字元，而不是跳脫字元。
print("hello,\" world!") # " (雙引號) 將雙引號成一般字元，而不是跳脫字元。


# r-string(原始字串)的練習：在字串前加上r，將反斜線當成一般字元，而不是跳脫字元。
# 可快速的解除所有跳脫字元可能產生的問題，常用於路徑表示。
print("hello,\n world!") 
print(r"hello,\n world!") 
print(r"C:\Users\08ethan\Python")

# Python 字串的運算： 
# 1. 串列化：將字串拆解成單一字元，放入 list (串列)中
# 2. 字串相乘：將字串重複顯示n次

s1 = 'hello'
s2 = 'world'
s = s1 + s2  # 串列化 s = s1 + s2
print(s)

s1 = "test"
print(s1*60) # 字串相乘：將字串重複顯示60次

# ====================================================================
# 字串切片 Slicing 從字串中取出特定部分。
# 基本語法為 [start:end:step]，其核心概念包含包前不包後、負數索引與間隔步長。
# 基本概念與寫法基本語法：text[start:end]，代表從開始位置取到結束位置前一個字（包前不包後）。
# 省略邊界：若省略 start 代表從頭開始（[:end]）；若省略 end 代表取到結尾（[start:]）。
# 負數索引：使用負數（如 -1）表示從字串最後一個字開始算起，方便取得結尾字元。
# 間隔步長 (Step)：第三個參數 [start:end:step] 用來控制跳著取或將字串反轉（如 [::-1]）。
# 常見範例:字串 s = "Hello"：s[1:4] 會得到 "ell"（索引 1、2、3）。s[:3] 會得到 "Hel"（從頭取到索引 2）。s[2:] 會得到 "llo"（從索引 2 取到結尾）。s[-2:] 會得到 "lo"（從倒數第二個字取到結尾）

s = "hello world"

print("=== 1. 您提供的基礎範例 ===")
print(f"s[1:4]  的結果是: '{s[1:4]}'")   # 得到 "ell"（索引 1、2、3）
print(f"s[:3]   的結果是: '{s[:3]}'")    # 得到 "Hel"（從頭取到索引 2）
print(f"s[2:]   的結果是: '{s[2:]}'")    # 得到 "llo"（從索引 2 取到結尾）
print(f"s[-2:]  的結果是: '{s[-2:]}'")   # 得到 "lo"（從倒數第二個字取到結尾）

print("\n=== 2. 延伸進階範例 ===")
print(f"s[::2]  (每隔兩字取一): '{s[::2]}'")   # 得到 "Hlo"
print(f"s[::-1] (字串完全反轉): '{s[::-1]}'")  # 得到 "olleH"
print(f"s[:100] (超出索引範圍): '{s[:100]}'")  # 得到 "Hello"（不報錯）

# slicing [start:end:step] 的應用練習： 注意stop索引不包含在內，step為取值的規則

s = "Hello world"
#    012345678910
#   -11~~~~~~  ~1
# 本例的索引值: -11 ~ +10

s1 = s[1:9:2] # 從正向取值的結果
print(s1)

s1 = s[-10:-2:2]  #從反向取值的結果和上面一樣 (由右到左取值)
print(s1)

# 反向取值：由step + 或 - 數值決定取值的方向

s2 = s[7:0:-2]
print(s2)

# 把原始資料做inverse (反轉) 倒著印出來 (step= -1)
s3 = s[-1::-1]
print(s3)

# 全部取值
s4 = s[::-1]
print(s4)

# 變大寫
s = "hello world"     
print(s.upper()) # 變大寫

s = "HELLO WORLD"    
print(s.lower()) # 變小寫

s2 = "hello world"     
s3 = s2.capitalize()
print(f"s3:(s3)")


# split(): 以空格為預設分隔符，將字串切成 list (串列) 
l1 = s.split() # 用空格當作分隔符，將字串切成 list
print(l1)

l1 = s.split("o") # 用o當作分隔符，將字串切成 list
print(l1)


# replace(): 將字串中的特定字串取代
s = "hello world"     
s1 = s.replace('l','--')  # ????
print(f"s1: {s1}")


# strip(): 去除字串前後的空白字符(不會刪除中間的空白)
s = "   hello world   "     
s1 = s.strip()
print(f"s1: {s1}")


# 搜尋子字串/關鍵字
s = "afdsfyihjdaidfxdhznduww1234djfidajf2s"
s1 = s.find("da")
print(f"s1: {s1}")  #找到後會回覆第一組符合的index位置
s1 = s.find("999")
print(f"s1: {s1}")  #找不到符合條件時，會回覆-1(代表直到最後都沒有)


