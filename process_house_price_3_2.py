import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
数据离散化第二部分：作图分析
0-40000 较低价格 25%分位以下
40000-64000 中等价格  25%分位至75%分位
64000-100000 较高价格 75%分位至超高价格阈值
100000以上 超高价格 根据密度分布图分析得出该阈值
'''

df = pd.read_csv('csvResult/Beijing_new_house_price_in_range.csv', encoding='utf-8')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
sections = [0, 40000, 64000, 100000, np.inf]  # 划分为不同长度的区间

price_level = ['较低价格', '中等价格', '较高价格', '超高价格']

explode = [0, 0, 0, 0.1]

# 按价格区间分割
result = pd.cut(df['average_price'], sections, labels=price_level)
print(result)
price_count = pd.value_counts(result, sort=False)  # 得到各部分的数量
print(price_count)

# 若无某个等级的数据则将该等级在图中删除，同时需要同步更新标签和拼图样式
price_count_copy = price_count.copy()
price_level_copy = price_level.copy()
explode_copy = explode.copy()
for i in range(len(price_count_copy)):
    if price_count_copy[i] == 0:
        price_level.remove(price_level_copy[i])
        explode.remove(explode_copy[i])
price_count = price_count[0 != price_count.values]

for i in range(len(price_level)):
    price_level[i] += (': ' + str(price_count[i]) + '个')

patches, l_text, p_text = plt.pie(price_count, explode=explode, labels=price_level, autopct='%1.2f%%',
                                  labeldistance=1.05)
plt.title('北京楼盘每平米单价离散化分析结果')
plt.axis('equal')
# 图例
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('figResult/data_discretization.png')
plt.show()
