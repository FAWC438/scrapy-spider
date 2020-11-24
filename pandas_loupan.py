import pandas as pd

fd = pd.read_csv('CsvData.csv')
print(fd)

print('-' * 25 + 'head' + '-' * 25)
print(fd.head())

print('-' * 25 + 'describe' + '-' * 25)
print(fd.describe())

print('-' * 25 + 'info' + '-' * 25)
print(fd.info())

print('-' * 22 + '按照总价升序' + '-' * 22)
print(fd.sort_values('total_price', inplace=False))

print('-' * 22 + '按照单价升序' + '-' * 22)
print(fd.sort_values('average_price', inplace=False))
