from matplotlib.container import PieContainer
from sklearn.datasets import load_iris

# 先產生資料集物件
iris_dataset = load_iris()

X = iris_dataset.data
print(f"x: {X}")

y = iris_dataset.target
print(f"y: {y}")
