import pandas as pd

df = pd.read_csv('csvData/BeijingPM20100101_20151231.csv', encoding='utf-8')

# 删去无用数据（行）
df.drop(['DEWP', 'HUMI', 'PRES', 'cbwd', 'Iws', 'precipitation', 'Iprec'], axis=1, inplace=True)
# 删去全部PM数据都不存在的行
df.dropna(axis=0, how='all', subset=['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post'], inplace=True)
# 线性插值
df['PM_Dongsi'] = df['PM_Dongsi'].interpolate()
df['PM_Dongsihuan'] = df['PM_Dongsihuan'].interpolate()
df['PM_Nongzhanguan'] = df['PM_Nongzhanguan'].interpolate()
df['PM_US Post'] = df['PM_US Post'].interpolate()
# 计算PM值的平均数
df['sum'] = df[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].sum(axis=1)
df['count'] = df[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].count(axis=1)  # count只会记录非空数据
df['average'] = round(df['sum'] / df['count'], 2)
print('*' * 20 + 'redued data' + '*' * 20)
print(df.info())

df_year = df.groupby('year').mean()
df_year.drop(df_year.columns[tuple([range(0, 12)])], axis=1, inplace=True)
print('*' * 20 + 'year data' + '*' * 20)
print(df_year.info())

df_month_pm = df.groupby('month').mean()
df_month_temp = df_month_pm.copy()

df_month_pm.drop(df_month_pm.columns[tuple([range(0, 12)])], axis=1, inplace=True)
print('*' * 20 + 'month data(PM)' + '*' * 20)
print(df_month_pm.info())

df_month_temp.drop(df_month_temp.columns[tuple([[i for i in range(0, 13) if i != 9]])], axis=1, inplace=True)
print('*' * 20 + 'month data(TEMP)' + '*' * 20)
print(df_month_temp.info())

df.to_csv("csvResult/Beijing_reduced_data_interpolate.csv")
df_year.to_csv("csvResult/Beijing_year_data_interpolate.csv")
df_month_pm.to_csv("csvResult/Beijing_month_pm_data_interpolate.csv")
df_month_temp.to_csv("csvResult/Beijing_month_temp_data_interpolate.csv")
