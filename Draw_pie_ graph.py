import matplotlib.pyplot as plt
import pandas as pd

'''
0-50 Ⅰ 优
51-100 Ⅱ 良
101-150 Ⅲ 轻度污染
151-200 Ⅳ 中度污染
201-300 Ⅴ 重度污染
>300 Ⅵ 严重污染
'''

pollution_level = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
pollution_count = [0, 0, 0, 0, 0, 0]
explode = [0, 0, 0.1, 0.1, 0.1, 0.1]

df = pd.read_csv('csvResult/Cities_PM_2015.csv', encoding='utf-8')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率

#
# fig = plt.figure()
# ax_beijing = fig.add_subplot(2, 3, 1)
# ax_shanghai = fig.add_subplot(2, 3, 2)
# ax_guangzhou = fig.add_subplot(2, 3, 3)
# ax_shenyang = fig.add_subplot(2, 3, 4)
# ax_chengdu = fig.add_subplot(2, 3, 5)
#
# for i in df['Beijing']:
#     if 0 <= i <= 50:
#         pollution_count[0] += 1
#     elif 50 < i <= 100:
#         pollution_count[1] += 1
#     elif 100 < i <= 150:
#         pollution_count[2] += 1
#     elif 150 < i <= 200:
#         pollution_count[3] += 1
#     elif 200 < i <= 300:
#         pollution_count[4] += 1
#     elif i > 300:
#         pollution_count[5] += 1
#     else:
#         raise Exception('负的PM值')
#
# ax_beijing.pie(pollution_count, labels=pollution_level, autopct='%1.1f%%')
# ax_beijing.set_title('北京空气质量分级天数图')

# for i in df['Beijing']:
for i in df['Chengdu']:
    if 0 <= i <= 50:
        pollution_count[0] += 1
    elif 50 < i <= 100:
        pollution_count[1] += 1
    elif 100 < i <= 150:
        pollution_count[2] += 1
    elif 150 < i <= 200:
        pollution_count[3] += 1
    elif 200 < i <= 300:
        pollution_count[4] += 1
    elif i > 300:
        pollution_count[5] += 1
    else:
        raise Exception('负的PM值')

# 若无某个等级的数据则将该等级在图中删除
pollution_count_copy = pollution_count.copy()
pollution_level_copy = pollution_level.copy()
explode_copy = explode.copy()
for i in range(len(pollution_count_copy)):
    if pollution_count_copy[i] == 0:
        pollution_count.remove(pollution_count_copy[i])
        pollution_level.remove(pollution_level_copy[i])
        explode.remove(explode_copy[i])

patches, l_text, p_text = plt.pie(pollution_count, explode=explode, labels=pollution_level, autopct='%1.2f%%')
plt.title('2015年成都空气质量分级天数占比图')
plt.axis('equal')
plt.legend(loc='upper left')

# 设置饼图内文字大小
for t in p_text:
    t.set_size(6)

plt.savefig('figResult/Chengdu.png')
plt.show()
