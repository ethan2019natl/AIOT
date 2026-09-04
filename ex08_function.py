# 115.08.10 練習-function
# 使用key：deg
# 組成: (1) function name  
#       (2) do something
#       (3) input
#       (4) output


# 定義函數


# type1: 沒有輸入輸出
def hello():
    '''
    無輸入
    無輸出
    列印字串
    '''
print("hello!")

# 使用工具(函式):呼叫名稱
hello()

# 查詢工具(函式):使用help()查詢
help(hello)



# type2: 有輸入輸出
def add(a,b):
    s = a + b
    return s

add(1,2)

print(add(1,2))
