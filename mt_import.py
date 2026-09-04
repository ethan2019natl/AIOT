import math

# 四捨五入
print(round(3.14))
print(math.ceil(3.14))
print(math.pi)


import random

print(random.random()) # 0~1的浮點數
print(random.randint(1, 10)) # 包含區間的隨機整數

# 均勻分布
print(random.uniform(1.0, 10.0))

# 指定不連續範圍的隨機數
print(random.choice([1, 3, 5, 6, 20, 100]))

l1 = [1,2,3,4,5,6]
random.shuffle(l1)
print(f"l1:{l1}")


import statistics
data = [i for i in range(10)]

print(f"mean: {statistics.mean(data)}")
print(f"median: {statistics.median(data)}")
print(f"mode: {statistics.mode(data)}")
print(f"variance: {statistics.variance(data)}")
print(f"stdev: {statistics.stdev(data)}")


# 統計
import statistics
import random
import matplotlib.pyplot as plt

# 丟硬幣實驗
# 樣本數
num_flips = 1000

# 每次丟硬幣的結果(正 & 反)
results = []

# 累計的平均值
running_means = []

# 模擬丟1000次硬幣
# 公平公正
# for i in range(num_flips):
#     # 隨機產生正(1)反(0)
#     result = random.randint(0, 1)

#     # 紀錄結果
#     results.append(result)

#     # 計算累計的平均
#     mean = statistics.mean(results)

#     # 紀錄累計的平均
#     running_means.append(mean)

# 不公平
results = [random.choices([0,1], [0.4, 0.6])[0] for _ in range(num_flips)]
running_means = [statistics.mean(results[:i+1]) for i in range(num_flips)]

print(f"results: {results[:10]}")
print(f"running_means: {running_means[:10]}")

# 繪製圖表
# 先產生畫布
plt.figure()

visual_num = 1000
# 先繪製點圖
plt.scatter(
    range(1, visual_num+1),# x data
    running_means[:visual_num],# y data
    marker='o',
    cmap='cool'
)
# 將資料點用線連結
plt.plot(
    range(1, visual_num+1),# x data
    running_means[:visual_num],# y data
    label="running mean" # 資料所代表的意義
)

# 繪製水平線
plt.axhline(0.5, color='r', linestyle="--", label='mean=0.5')

# 定義名稱
# X軸名稱
plt.xlabel('number of coin flips')
# y軸名稱
plt.ylabel('running mean')
# 圖表名稱
plt.title("figure of running mean")
# 顯示定義在圖表中的label
plt.legend()
# 儲存圖表
plt.savefig("figure.jpg")
# 顯示圖表
plt.show()