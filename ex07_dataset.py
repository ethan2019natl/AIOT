# 115.08.10 練習-資料處理
#
# 先安裝套件：pip install -U scikit-learn

# pyrefly: ignore [missing-import]
from matplotlib.container import PieContainer
from sklearn.datasets import load_iris  #載入iris資料集(鳶尾花資料集)

# 先產生資料及物件

iris_dataset = load_iris()  #把iris資料集產生在iris_dataset這個物件裡

x = iris_dataset.data       #把特徵值(數字)產生在x這個物件裡
print(f"x: {x}")  

y = iris_dataset.target     #把標籤值(類別)產生在y這個物件裡
print(f"y: {y}")







