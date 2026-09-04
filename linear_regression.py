import random # 產生隨機數
import statistics # 計算統計參數
from statistics import StatisticsError # 統計上的error
from collections import namedtuple # 建立簡單的資料型的類別(tuple)

# 使用nametuple 定義一個 Linear Regression 結果(取得的m, b)的類別
linearRegression = namedtuple('LinearRegression', ['slope', 'intercept'])

def linear_regression(x, y, proportional=False):
    '''
        y = m*x + b, m=slope, b=intercept
    '''
    # 檢查資料正確性
    # 1. 檢查x, y data數量有沒有一樣
    n = len(x)

    if len(y) != n:
        raise StatisticsError('x data數量與y data不一樣多')

    # 2. 檢查data數量 >= 2
    if n < 2:
        raise StatisticsError('資料點數必須大於2')

    # 通過原點
    if proportional:
        # 協方差
        sum_xy = statistics.fsum(xi * yi for xi, yi in zip(x, y))
        # 變異數
        sum_xx = statistics.fsum(xi**2 for xi in x)

        # 檢查變異數是否為0
        if sum_xx == 0:
            raise StatisticsError("變異數 sum_xx 為0")

        # 斜率 m 
        slope = sum_xy / sum_xx
        # 截距 b
        intercept = 0.0
    else: # 沒有通過原點
        # 計算x, y平均
        x_mean = statistics.fsum(x)/n
        y_mean = statistics.fsum(y)/n

        # 協方差
        sum_xy = statistics.fsum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        # 變異數
        sum_xx = statistics.fsum((xi - x_mean)**2 for xi in x)

        try:
            slope = sum_xy/sum_xx
        except ZeroDivisionError: # 抓捕特定錯誤
            # 自訂義錯誤內容
            raise StatisticsError("變異數 sum_xx 為0")

        intercept = y_mean - slope * x_mean

    return linearRegression(slope=slope, intercept=intercept)

# 實際的斜率
TRUE_SLOPE = 2.75
# 實際的截距
TRUE_INTERCEPT = 12.345
# 資料點數
NUM_SAMPLES = 100
# 雜訊的波動程度
NOISE_STRENGHT = 1.5

# 生成模擬的數據
X_data = [random.uniform(1, 50) for _ in range(NUM_SAMPLES)]

Y_data = []
for x in X_data:
    true_y = TRUE_SLOPE * x + TRUE_INTERCEPT

    # 產生雜訊
    noise = random.gauss(0, NOISE_STRENGHT)

    # 產生觀察值
    Y_data.append(true_y + noise)

try:
    res = linear_regression(X_data, Y_data)
    print(f"預估的 y = {res.slope:.3f} * x + {res.intercept:.3f}")
    print(f"真實的 y = {TRUE_SLOPE} * x + {TRUE_INTERCEPT}")

except StatisticsError as e:
    print(f"error: {e}")