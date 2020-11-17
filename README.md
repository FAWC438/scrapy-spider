# scrapy-spider

基于 Scrapy 的网页数据爬取

## 1. 题目要求

### 1.1 爬取学堂在线的计算机类课程页面内容

<https://www.xuetangx.com/search?query=&org=&classify=1&type=&status=&page=1>

要求将课程名称、老师、所属学校和选课人数信息，保存到一个 csv 文件中。

### 1.2 爬取链家官网二手房的数据

<https://bj.lianjia.com/ershoufang/>

要求爬取北京市东城、西城、海淀和朝阳四个城区的数据（每个区爬取 5 页），将楼盘名称、总价、平米数、单价保存到 json 文件中。

> 以上作业以报告形式提交，需要将核心代码贴在报告中，并在报告中给出最终的 csv 和 json 文件内容（截取前 50 条数据即可）。文件名为学号，文件格式为 pdf。

## 2. 需求分析

### 2.1 学堂在线

在浏览器打开链接

<https://www.xuetangx.com/search?query=&org=&classify=1&type=&status=&page=1>

后显示如图 1 所示页面，其中的相关元素能够容易地获得其 xpath

![alt text](https://note.youdao.com/yws/api/personal/file/WEBf56310f9739742ebc5164b372378a0c5?method=download&shareKey=3c7c7802315c96714a514ab2639c4d82 "图1 学堂在线主页面")

但是，查看网页源代码（图 2）后可以发现，该页面由 js 动态生成，无法用传统**静态页面 + xpath**的方法爬取数据。

![alt text](https://note.youdao.com/yws/api/personal/file/WEBec810df566a88d8fbed18f9f186ef3a8?method=download&shareKey=9217ef7a1ce65da6a64821b6fad8940b "图2 学堂在线网页源码")

刷新页面，并在浏览器开发者工具中的网页选项查看资源请求情况，发现一个 **XMLHttpRequest**（图 3），其 POST 请求返回有关页面内所有数据（包括未显示的数据）的 JSON。

![alt text](https://note.youdao.com/yws/api/personal/file/WEB0b9f0efdd698030e5e96ab078c294f1b?method=download&shareKey=cacf448b2c1052e5c070d835fba4555b "图3 返回JSON数据的XHR")

因此，本实验中应当利用 Scrapy 向图 3 中**XMLHttpRequest**对应的 URL 发送 POST 请求，通过解析返回的 JSON 数据得到课程的具体信息，进而在 Scrapy 的**piplines**中将数据写入 CSV。

### 2.2 链家

在浏览器打开链接

<https://bj.lianjia.com/ershoufang/>

后显示如图 4 所示页面，其中的相关元素能够容易地获得其 xpath

![alt text](https://note.youdao.com/yws/api/personal/file/WEBee170a0eb09c991f6e19c58b9512b661?method=download&shareKey=d97473336092a384d145d4a28e4913bc "图4 链家主页面")

链家的网页资源为静态页面，即通过浏览器的 URL 发送 GET 请求即可获取整个页面的 HTML 资源。然而在测试中发现，利用浏览器开发工具自动生成的绝对 xpath 存在无法获取数据的问题。因此在该部分的 xpath 将利用间接定位的间接 xpath 定位有关元素，进而在 Scrapy 的**piplines**中将数据写入 JSON 文件。

## 3. 程序设计

### 3.1 Spider-学堂在线

类 `XuetangSpider` 是学堂在线的爬虫代码主体部分，该部分有成员变量如下：

```python
name = 'xuetang'
allowed_domains = ['xuetangx.com']
base_url = 'https://www.xuetangx.com/api/v1/lms/get_product_list/?page='
page_index = 1
headers = {
    'accept': 'application/json,text/plain,*/*',
    …
}
payload = {'query': "", 'chief_org': [], 'classify': ["1"], 'selling_type': [], 'status': [], 'appid': 10000}
```

其中，`base_url` 来源于对应的 **XMLHttpRequest**，`headers` 的内容是在清除浏览器缓存和 Cookie 后在开发者工具中获取的；`payload` 是在浏览器开发者工具中得到的 POST 请求负载。

还需要重写类 `XuetangSpider` 的构造函数，以更改爬虫的爬取时间间隔（设为 1 秒），防止网站反爬机制阻止爬取数据。

`parse` 函数处理了返回的 JSON 数据，并将其设置为 items.py 中设定的数据格式，传送到 pipelines.py 以进行后续处理；同时也实现了翻页功能，对每一个页面请求 POST 数据直到页面结束为止。

另外，重写了 `start_requests` 函数，确保了爬虫在首次执行时对第一个页面发送 POST 请求。由于重写了该方法，成员变量中无需含有 `start_urls`。

### 3.2 Spider-链家

类 `LianjiaSpider` 是链家的爬虫代码主体部分，该部分有成员变量如下：

```python
name = 'lianjia'
allowed_domains = ['bj.lianjia.com']
base_url = 'https://bj.lianjia.com/ershoufang/'
zones = ['dongcheng/', 'xicheng/', 'chaoyang/', 'haidian/']
zones_chinese = ['东城', '西城', '朝阳', '海淀']
page_index = 1  # 页面计数
zone_index = 1  # 地区计数
start_urls = [base_url + zones[0]]
```

同样地，需要重写类 `LianjiaSpider` 的构造函数，由于链家的反爬机制更为严格，爬虫的爬取时间间隔应当设为 5 秒。

`parse` 函数通过 xpath 定位响应的相应元素，利用正则表达式等工具，将其处理为 items.py 中设定的数据格式，传送到 pipelines.py 以进行后续处理；同时也实现了翻页功能和地区切换功能，对每一个地区的前 5 个页面请求数据。

## 4. 程序使用说明

### 4.1 开发/运行环境

_**IDE**_：PyCharm 2020.2.3 (Professional Edition)

_**操作系统**_：Windows 10 (version: 20H2)

_**Python 版本**_：Python 3.8

### 4.2 文件说明

    scrapyProject
    ├── CsvData.csv
    ├── JsonData.json
    ├── run.py
    ├── README.md
    ├── scrapy.cfg
    ├── 作业要求.txt
    └── scrapyProject
        ├── _init_.py
        ├── items.py
        ├── middlewares.py
        ├── piplines.py
        ├── settings.py
        └── spiders
            ├── _init_.py
            ├── bupt.py
            ├── lianjia.py
            └── xuetang.py

本实验的文件树如上所示。

数据结果分别存于**CsvData.csv**和 **JsonData.json** 中。**run.py** 是项目的运行入口。**scrapyProject** 文件夹是 Scrapy 的项目文件，项目入口<b>\_init\_.py</b> 和中间件 **middlewares.py** 在本次实验中没有使用，**items.py** 设定了爬取数据的内容格式，**piplines.py** 设定了爬取数据的输出方式，**settings.py** 则对项目部的分属性进行了全局设置。

**spiders** 文件夹保存了三个主要的爬虫文件，**bupt.py** 是课上所给的爬取学校学院信息的例子的修改版本；**lianjia.py** 是链家的爬虫文件；**xuetang.py** 是学堂在线的爬虫文件。

### 4.3 运行说明

建议在集成开发环境 **PyCharm** 中运行本项目。

![alt text](https://note.youdao.com/yws/api/personal/file/WEB63d2306aa83f166daf5e7c8ef3e9abdf?method=download&shareKey=b3a6bd89d3d2c1c23763ae4c85e412c6 "图5 Scrapy的安装")

在 PyCharm 的项目中，找到设置中的图 5 界面。点击该界面点击右方的 **'+'** 符号，搜索 _**Scrapy**_ 并安装，可以大大简化 Scrapy 的安装过程。

安装完毕后，直接运行 run.py 即能运行本项目。若要分别运行三个不同的爬虫，按照 run.py 中的注释修改代码即可。
