import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

'''
数据离散化第一部分：分析分组依据
'''

df = pd.read_csv('csvResult/Beijing_new_house_price_in_range.csv', encoding='utf-8')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
fig = plt.figure()
average_price_mean = df['average_price'].mean()
average_price_std = df['average_price'].std()

print(df.describe())

'''
kstest方法：KS检验，参数分别是：待检验的数据，检验方法（这里设置成norm正态分布），均值与标准差
结果返回两个值：statistic → D值，pvalue → P值
H0:样本符合正态分布
H1:样本不符合正态分布 
若p>0.05接受H0 ,反之
'''
res = stats.kstest(df['average_price'], 'norm', (average_price_mean, average_price_std))
print(res)

print(average_price_mean - 0.5 * average_price_std, average_price_mean + 0.5 * average_price_std)  # 38%的数据
print(average_price_mean - 1 * average_price_std, average_price_mean + 1 * average_price_std)  # 68%的数据
print(average_price_mean - 2 * average_price_std, average_price_mean + 2 * average_price_std)  # 95%的数据
print(average_price_mean - 3 * average_price_std, average_price_mean + 3 * average_price_std)  # 99%的数据

# 数据直方图
df['average_price'].hist(bins=50, alpha=0.5)
'''
核密度估计图
它是通过计算“可能会产生观测数据的连续概率分布的估计”而产生的。
一般的过程是将该分布近似为一组核（即诸如正态（高斯）分布之类的较为简单的分布）。
因此，密度图也被称作KDE（Kernel Density Estimate,核密度估计）图。
调用plot时加上kind='kde'即可生成一张密度图
'''
df['average_price'].plot(kind='kde', secondary_y=True)
plt.title('北京楼盘均价数据分布图')

plt.tight_layout()
plt.savefig('figResult/data_distribution.png')
plt.show()
