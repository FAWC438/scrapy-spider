import pandas as pd

'''
去除异常数据
'''

df = pd.read_csv('csvData/Beijing_new_house_price.csv', encoding='utf-8')

print("--------------head--------------")
print(df.head())
print("--------------describe--------------")
print(df.describe())
print("--------------info--------------")
print(df.info())
print("================================")

total_price_mean = df['total_price'].mean()
total_price_std = df['total_price'].std()

print(total_price_mean - 3 * total_price_std, total_price_mean + 3 * total_price_std)
# 小于三倍标准差为负数，不可能出现，因此只考虑大于三倍标准差的情况

# 删去总价大于均值三倍标准差的行，得到范围内的数据
df_in_range = df.drop(df[df['total_price'] > total_price_mean + 3 * total_price_std].index)
# 删去总价小于等于均值三倍标准差的行，得到范围外的数据
df_out_range = df.drop(df[df['total_price'] <= total_price_mean + 3 * total_price_std].index)

print("--------------head--------------")
print(df_out_range.head())
print("--------------describe--------------")
print(df_out_range.describe())
print("--------------info--------------")
print(df_out_range.info())
print("================================")
print('异常数据总数：' + str(df_out_range.index.size))

df_in_range.to_csv('csvResult/Beijing_new_house_price_in_range.csv', encoding='utf_8_sig', index=False)
df_out_range.to_csv('csvResult/Beijing_new_house_price_out_range.csv', encoding='utf_8_sig', index=False)
