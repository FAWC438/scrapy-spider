import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

'''
数据归一化
'''

df = pd.read_csv('csvResult/Beijing_new_house_price_in_range.csv', encoding='utf-8')
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率

fig = plt.figure()
scaler = MinMaxScaler()
scaler_std = StandardScaler()

# 原始数据
ax1 = fig.add_subplot(1, 3, 1)
x1 = df["total_price"]
y1 = df["average_price"]
ax1.scatter(x1, y1, s=10)
ax1.set_xlabel("Total price")
ax1.set_ylabel("Average price")
ax1.set_title("Original Data")

x_reshape = x1.values.reshape(-1, 1)  # 变成n行1列的二维矩阵形式
y_reshape = y1.values.reshape(-1, 1)  # 变成n行1列的二维矩阵形式
# 0-1归一化
ax2 = fig.add_subplot(1, 3, 2)
x2 = scaler.fit_transform(x_reshape)
y2 = scaler.fit_transform(y_reshape)
ax2.scatter(x2, y2, s=10)
ax2.set_xlabel("Total price")
ax2.set_ylabel("Average price")
ax2.set_title("MinMaxScaler Data")

# Z-score归一化
ax3 = fig.add_subplot(1, 3, 3)
x3 = scaler_std.fit_transform(x_reshape)
y3 = scaler_std.fit_transform(y_reshape)
ax3.scatter(x3, y3, s=10)
ax3.set_xlabel("Total price")
ax3.set_ylabel("Average price")
ax3.set_title("StandardScaler Data")

plt.tight_layout()
plt.savefig('figResult/normalize.png')
plt.show()
