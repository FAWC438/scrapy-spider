import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
通过CSV文件数据作饼图

0-50 Ⅰ 优
51-100 Ⅱ 良
101-150 Ⅲ 轻度污染
151-200 Ⅳ 中度污染
201-300 Ⅴ 重度污染
>300 Ⅵ 严重污染
'''

df = pd.read_csv('csvResult/Cities_PM_2015.csv', encoding='utf-8')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
sections = [0, 50, 100, 150, 200, 300, np.inf]  # 划分为不同长度的区间

cities = {'Beijing': '北京', 'Shanghai': '上海', 'Guangzhou': '广州', 'Shenyang': '沈阳', 'Chengdu': '成都'}

for k, v in cities.items():
    print(v)
    pollution_level = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
    explode = [0, 0, 0.1, 0.1, 0.1, 0.1]

    # 按空气质量区间分割
    result = pd.cut(df[k], sections, labels=pollution_level)
    pollution_count = pd.value_counts(result, sort=False)  # 得到各部分的数量

    # 若无某个等级的数据则将该等级在图中删除，同时需要同步更新标签和饼图样式
    pollution_count_copy = pollution_count.copy()
    pollution_level_copy = pollution_level.copy()
    explode_copy = explode.copy()
    for i in range(len(pollution_count_copy)):
        if pollution_count_copy[i] == 0:
            pollution_level.remove(pollution_level_copy[i])
            explode.remove(explode_copy[i])
    pollution_count = pollution_count[0 != pollution_count.values]

    for i in range(len(pollution_level)):
        pollution_level[i] += (': ' + str(pollution_count[i]) + '天')

    patches, l_text, p_text = plt.pie(pollution_count, explode=explode, labels=pollution_level, autopct='%1.2f%%')
    plt.title('2015年' + v + '空气质量分级天数占比图')
    plt.axis('equal')
    # 图例
    plt.legend(loc='upper left')

    # 设置饼图内文字大小
    for t in p_text:
        t.set_size(6)

    plt.tight_layout()
    plt.savefig('figResult/' + k + '.png')
    plt.show()
