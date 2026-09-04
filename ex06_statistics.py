# 115.08.10 練習-統計

import enum
import statistics
data = [i for i in range(10)]
print(f"data: {data}")
print(f"mean: {statistics.mean(data)}") # 平均
print(f"mode: {statistics.mode(data)}") # 眾數
print(f"stdev: {statistics.stdev(data)}") # 標準差
print(f"variance: {statistics.variance(data)}") # 方差

# 統計
import statistics
import random
import matplotlib.pyplot as plt #繪圖套件，並用as指令取暱稱為plt

# 安裝第三方套件 (模組)
# 在命令列輸入 pip install matplotlib

# 丟硬幣實驗
num_flips = 1000    # 實驗次數(樣本數)=1000
results = []        # 每次丟硬幣的結果(正面或反面) 暱稱
running_means = []   # 累計平均值

for i in range(num_flips):          #模擬丟1000次
    result = random.randint(0,1)    #隨機產生0或1，正面為1，反面為0
    results.append(result)          #將結果記錄到results列表中
    mean = statistics.mean(results) #計算累計平均值
    running_means.append(mean)      #將累計平均值記錄到running_means列表中

# 不公平
results = [random.choices([0,1],[0.4,0.6],k=1)[0] for _ in range(num_flips)] #不公平機率1正面0反面，機率0.4
running_means = [statistics.mean(results[:i+1]) for i in range(num_flips)]


print(f"results: {results[:10]}")
print(f"running_means: {running_means[:10]}")
    
# 繪製圖表
plt.figure() #先產生畫布
visual_num = 1000  #繪製點圖(1000個點)

#繪製點圖(100個點)
plt.scatter(    
    range(1,visual_num+1) ,#X軸為試驗次數，
    running_means[:visual_num] ,# Y軸為累計平均值
    marker='o' ,#點的形狀
    cmap='cool'
)

# 繪製水平線(當作二分之一的參考線)
plt.axhline(0.5, color = 'r', linestyle = '--', label = 'mean = 0.5')

#定義名稱
plt.xlabel("number of coin flips") #X軸標籤
plt.ylabel("running mean") #Y軸標籤
plt.title("figuer of running mean") #圖表標題

# 顯示圖表
plt.show()

# 儲存圖表
plt.savefig("figure.png")







