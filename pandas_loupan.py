import pandas as pd

fd = pd.read_csv('CsvData.csv', delimiter="\t", encoding='GBK')
print(fd)

print('-' * 24 + '简介' + '-' * 24)
print(fd.describe())

print('-' * 22 + '按照总价升序' + '-' * 22)
print(fd.sort_values('total_price', inplace=False))

print('-' * 22 + '按照单价升序' + '-' * 22)
print(fd.sort_values('average_price', inplace=False))
