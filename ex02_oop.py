# 115.08.03 練習 oop (物件導向程式設計)
# 字串的格式化表示法
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


