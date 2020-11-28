import pandas as pd
from pandas import DataFrame

df_res = DataFrame()

# 北京数据
df = pd.read_csv('csvData/BeijingPM20100101_20151231.csv', encoding='utf-8')
# print(df.info())
# 删去无用数据（行）
# df.drop(['DEWP', 'HUMI', 'PRES', 'cbwd', 'Iws', 'precipitation', 'Iprec'], axis=1, inplace=True)
df.drop(df.columns[list(range(10, 18))], axis=1, inplace=True)
df.drop(df[df['year'] < 2015].index, inplace=True)
# 线性插值
df['PM_Dongsi'] = df['PM_Dongsi'].interpolate()
df['PM_Dongsihuan'] = df['PM_Dongsihuan'].interpolate()
df['PM_Nongzhanguan'] = df['PM_Nongzhanguan'].interpolate()
df['PM_US Post'] = df['PM_US Post'].interpolate()
# 删去全部PM数据都不存在的行
df.dropna(axis=0, how='all', subset=['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post'], inplace=True)
# 计算PM值的平均数
df['sum'] = df[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].sum(axis=1)
df['count'] = df[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].count(axis=1)  # count只会记录非空数据
df['average'] = round(df['sum'] / df['count'], 2)
# 通过月和日聚合
df = df.groupby(['month', 'day']).mean()
df_res['year'] = df['year'].astype(int)
df_res['Beijing'] = df['average']

# print('*' * 20 + 'redued data' + '*' * 20)
# print(df.info())
# print(df_res.info())
# print(df_res.head())

# 上海数据
df = pd.read_csv('csvData/ShanghaiPM20100101_20151231.csv', encoding='utf-8')
df.drop(df.columns[list(range(9, 17))], axis=1, inplace=True)
df.drop(df[df['year'] < 2015].index, inplace=True)
df['PM_Jingan'] = df['PM_Jingan'].interpolate()
df['PM_Xuhui'] = df['PM_Xuhui'].interpolate()
df['PM_US Post'] = df['PM_US Post'].interpolate()
df.dropna(axis=0, how='all', subset=['PM_Jingan', 'PM_Xuhui', 'PM_US Post'], inplace=True)
df['sum'] = df[['PM_Jingan', 'PM_Xuhui', 'PM_US Post']].sum(axis=1)
df['count'] = df[['PM_Jingan', 'PM_Xuhui', 'PM_US Post']].count(axis=1)  # count只会记录非空数据
df['average'] = round(df['sum'] / df['count'], 2)
df = df.groupby(['month', 'day']).mean()
df_res['Shanghai'] = df['average']

# 广州数据
df = pd.read_csv('csvData/GuangzhouPM20100101_20151231.csv', encoding='utf-8')
df.drop(df.columns[list(range(9, 17))], axis=1, inplace=True)
df.drop(df[df['year'] < 2015].index, inplace=True)
df['PM_City Station'] = df['PM_City Station'].interpolate()
df['PM_5th Middle School'] = df['PM_5th Middle School'].interpolate()
df['PM_US Post'] = df['PM_US Post'].interpolate()
df.dropna(axis=0, how='all', subset=['PM_City Station', 'PM_5th Middle School', 'PM_US Post'], inplace=True)
df['sum'] = df[['PM_City Station', 'PM_5th Middle School', 'PM_US Post']].sum(axis=1)
df['count'] = df[['PM_City Station', 'PM_5th Middle School', 'PM_US Post']].count(axis=1)  # count只会记录非空数据
df['average'] = round(df['sum'] / df['count'], 2)
df = df.groupby(['month', 'day']).mean()
df_res['Guangzhou'] = df['average']

# 沈阳数据
df = pd.read_csv('csvData/ShenyangPM20100101_20151231.csv', encoding='utf-8')
df.drop(df.columns[list(range(9, 17))], axis=1, inplace=True)
df.drop(df[df['year'] < 2015].index, inplace=True)
df['PM_Taiyuanjie'] = df['PM_Taiyuanjie'].interpolate()
df['PM_Xiaoheyan'] = df['PM_Xiaoheyan'].interpolate()
df['PM_US Post'] = df['PM_US Post'].interpolate()
df.dropna(axis=0, how='all', subset=['PM_Taiyuanjie', 'PM_Xiaoheyan', 'PM_US Post'], inplace=True)
df['sum'] = df[['PM_Taiyuanjie', 'PM_Xiaoheyan', 'PM_US Post']].sum(axis=1)
df['count'] = df[['PM_Taiyuanjie', 'PM_Xiaoheyan', 'PM_US Post']].count(axis=1)  # count只会记录非空数据
df['average'] = round(df['sum'] / df['count'], 2)
df = df.groupby(['month', 'day']).mean()
df_res['Shenyang'] = df['average']

# 成都数据
df = pd.read_csv('csvData/ChengduPM20100101_20151231.csv', encoding='utf-8')
df.drop(df.columns[list(range(9, 17))], axis=1, inplace=True)
df.drop(df[df['year'] < 2015].index, inplace=True)
df['PM_Caotangsi'] = df['PM_Caotangsi'].interpolate()
df['PM_Shahepu'] = df['PM_Shahepu'].interpolate()
df['PM_US Post'] = df['PM_US Post'].interpolate()
df.dropna(axis=0, how='all', subset=['PM_Caotangsi', 'PM_Shahepu', 'PM_US Post'], inplace=True)
df['sum'] = df[['PM_Caotangsi', 'PM_Shahepu', 'PM_US Post']].sum(axis=1)
df['count'] = df[['PM_Caotangsi', 'PM_Shahepu', 'PM_US Post']].count(axis=1)  # count只会记录非空数据
df['average'] = round(df['sum'] / df['count'], 2)
df = df.groupby(['month', 'day']).mean()
df_res['Chengdu'] = df['average']

df_res = df_res.round(2)
print(df.info())
print(df_res.info())
print(df_res.head())

df_res.to_csv('csvResult/Cities_PM_2015.csv')
