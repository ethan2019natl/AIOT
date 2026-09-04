
# 定義函式
# type1: 沒有輸入輸出
def hello():
    '''
    無輸入
    無輸出
    列印字串
    '''
    print("hello!")

# 使用工具(函式): 呼叫名稱
hello()

# 查詢工具
help(hello)

# type2: 有輸入輸出
def add(a, b):
    s = a+b
    return s

print(add(1,2))


# 多個回傳值: 以tuple型態回傳
def arithmatic(a, b):
    add = a+b
    sub = a-b 
    mul = a*b
    div = a/b
    return add, sub, mul, div

results = arithmatic(1,2)
print(f"results: {results}")
print(f"add: {results[0]}")

# tuple unpack:
my_add, sub, mul, div = arithmatic(1,2)
print(f"my_add: {my_add}")

# 函式做為回傳值
# 電商動態計價器
# 參數給預設值
def create_price_calculator(discount_rate, tax_rate=0.01):
    def calculator_price(base_price):
        discounted = base_price * (1-discount_rate)
        final_price = discounted * (1+tax_rate)
        return round(final_price, 0)

    return calculator_price

# 關鍵字參數的使用方法: key=value
vip_calc = create_price_calculator(tax_rate=0.05, discount_rate=0.2)
# 使用位置參數: (discount_rate, tax_rate)=(0.1, 0.05)
mem_calc = create_price_calculator(0.1, 0.05)
# 混搭使用方式: 位置參數先定義, 再定義關鍵字參數
nonmem_calc = create_price_calculator(0.05, tax_rate=0.05)
# 使用參數預設值
calc = create_price_calculator(0.05)

product_price = 1000

# 如何執行回傳的函式
print(f"VIP price : {vip_calc(product_price)}")
print(f"Member price : {mem_calc(product_price)}")
print(f"non Member price : {nonmem_calc(product_price)}")

print(f"VIP price : {create_price_calculator(tax_rate=0.05, discount_rate=0.2)(product_price)}")
print(f"Member price : {create_price_calculator(0.1, 0.05)(product_price)}")
print(f"non Member price : {create_price_calculator(0.05, tax_rate=0.05)(product_price)}")


# 全域變數 vs 區域變數
g_x = 0

def count():
    global g_x
    g_x += 1

    print(f"g_x: {g_x}")


count()
count()
count()


def count1():
    total = 0
    total += 1

    print(f"total: {total}")

count1()
count1()
count1()

# 再函式內讀取全域變數
a = 10
def f():
    print(f"a: {a}")

f()

# error
total = 0
# def count2():
#     total += 1
#     print(f"total: {total}")

# count2()


# 不定長度的參數: *
def multiply_all(*args):
    res = 1

    for num in args:
        res *= num

    return res

print(multiply_all(1,2,3,4,5,6))


def products(**keyargs):
    for product, price in keyargs.items():
        print(f"{product}: $ {price} 元")

products(milk=100, apple=10, banana=30)


# lambda function
f = lambda x: x**2
print(f(2))

print((lambda x: x**2)(2))

l1 = [1,2,3,4,5]
print(list(map(lambda x: x**2, l1)))