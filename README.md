﻿# GetDataFromTomatoReading
一、需求
爬取番茄小说网站的《小古文分级阅读天天练》（一年级到六年级）中古文标题、古文正文、古文选自文章，如下图所示。（本文以四年级为例）

二、设计思路概述
第一步：抓包分析，通过浏览器开发者工具进行抓包分析，判断需求数据所在的对应位置，并分析不同章节变化规律，以便于批量化数据采集。
第二步：发送请求并获取数据，先手动登录，并在网页抓包得到cookie值，便于后续的网站访问，再构造requests.get()请求中的其他字段。
第三步：解析数据，使用parsel提取古文标题、古文正文、古文选自文章三部分数据。
第四步：处理数据，对解析出的数据按照番茄的字体解密包，解密成unicode编码的数据，并对数据进行格式化，剔除无用数据，把有用数据处理成较为整洁的模式。
第五步：保存数据，把数据存储到对应的txt文件中。
三、代码思路
1.代码结构
Code
├─ const.py                    静态变量的设置
├─ grade_1_2.py                12年级古文下载
├─ grade_3_4_5_6.py            3456年级古文下载
├─ main.py                    主函数，可以下载全年级古文书籍
└─ utils.py                     工具类
2.const.py
是一些静态变量，包括各年级书籍的url，headers记录了User-Agent和cookie以及的番茄小说文本的解密字典。
3.grade_1_2.py
是12年级的书籍处理，代码流程：执行download_books()遍历url数组，在getData()中得到目标年级书籍的各个章节的url，然后遍历的去请求和解析数据，再通过write_title，write_text，write_article。三个方法，分别处理并保存古文的标题、正文和选自文章。（一本书对应三个txt文件）
4.grade_3_4_5_6.py
是3456年级的书籍处理，代码流程：执行download_books()遍历url数组，在getData()中得到目标年级书籍的各个章节的url，然后遍历的去请求和解析数据，再通过write_content方法处理并保存古文的标题、正文和选自文章。（一本书对应一个txt文件）
5.main.py
是主函数，可以通过调用grade_1_2和grade_3_4_5_6中的download_books()方法得到目标书籍的古文。
6.Utils.py
是一些工具函数，其中is_neither_chinese_nor_punctuation方法，用于判断字符串是否是中文或者标点，text_decode方法用于把获得的文本根据解密字典解码。
四、如何运行
# 跳转到当前目录
cd 目录名
# 先卸载依赖库
pip uninstall -y -r requirement.txt
# 再在清华镜像重新安装依赖库
pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 开始运行
python main.py
三、抓包分析
1.打开网络开发者工具
以牛郎织女篇为例，进入https://fanqienovel.com/reader/7350583901460368447，通过F12或者右键检查打开开发者工具，默认进入元素界面

2.分析数据包得到对应数据位置
通过ctrl+F关键字搜索或者手动判断的方式，找到古文标题、古文正文、古文选自文章。如下图所示，标题对应的是class=”chapter-three”，古文正文对应的是class=”bodytext”，古文选自文章对应的是class=”bodytext-right”（对应文本内容部分显示不全是因为番茄小说对一些字进行了加密操作，因此无法在页面上正常显示）

3.批量化数据采集
首先分析不同章节链接的变化规律，以获得
第一章url:https://fanqienovel.com/reader/7350583897182178343
第二章url:https://fanqienovel.com/reader/7350583898557926436
可以看出，不同章节间是通过reader/后的章节ID进行区分的，那么如何获得章节ID呢？可以访问书籍的目录页，在该页面打开网络开发者分析工具，并可以看到不同章节会对应不同元素内容，这里的元素内容中包括章节ID。<a href="/reader/7350583897182178343" class="chapter-item-title" target="_blank">女娲造人</a>，那么可以通过访问目录页的方式获得不同章节对应的跳转路由url，然后再遍历访问跳转路由，获取数据内容。

四、发送请求
1.第一次请求
根据目标书籍，设置好url和headers（包含cookie标签，从而可以登录进网站，还包括User-Agent字段模拟浏览器访问，避免被网站拦截），调用python中的requests包的get方法，发送请求，请求目标小说的目录页，并通过数据解析得到不同章节的跳转路由url。
ua ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
headers = {"User-Agent": ua, "Cookie": “cookie字段"}
response = requests.get(url=”目标书籍目录url”, headers=headers)
2.第二次请求
根据第一次请求得到的跳转路由和已设置好的headers，进行请求发送
response = requests.get(url=”目标书籍章节url”, headers=headers)
3.cookie的获取
先手动登录网页端番茄小说，在登录后打开网络开发工具，找到网络（network），通过ctrl+f搜索cookie，然后找到对应的cookie字段，并把后续cookie对应的所有内容（图中黄色部分）复制保存。即为cookie。从而可以登录访问网站。

五、解析数据
1.通过parsel提取数据
先得到selector
link_selector = parsel.Selector(link_data)
再通过.css()方法得到对应的内容，其中class=chapter-three对应的是古文标题，body::text对应的是古文的正文和杂数据（包括注释，问答的文本也在），bodytext-right::text对应的是古文文章。
content_list=link_selector.css("[class=chapter-three] ::text, .bodytext ::text, .bodytext-right ::text").getall()
六、处理数据
由于一二年级数据带有拼音，古文的文本格式与其他年级有较大不同，因此在数据处理的时候选择分别处理，一、二年级选择分别保存古文的标题、正文和选自文章。其他年级直接通过逻辑得到古文标题和正文之间的内容。
1.数据解密
由于番茄小说设置的反爬虫机制，对文本数据进行了加密，于是从网上找了该加密对应的unicode映射字典，放到了util包里。遍历解析的数据，如果在字典中能找到就转码，不在字典就维持原样。
2.一二年级的数据处理。
由于一二年级的古文拼音，而它在页面文本中与正文相混杂，导致直接截取标题到选自文章的方式较为困难，因此选自分别对古文标题、正文和选自文章进行处理。
（1）标题（grade_1_2.write_title()方法）
通过判断uincode码的方式，判断是否是中文或者标点符号，从而剔除注释标注符号，并且根据输出内容，适当调整换行。结果如下图所示

（2）正文（grade_1_2.write_text()方法）
输出发现原标签yinwen下的元素ruby下text只有古文，但是没有古文的标点符号，所以需要解析的内容除了.yinwen ruby text::还需要有yinwen::text。但是加上yinwen::text后又引入了古文翻译等杂数据。所以需要只记录正文数据，剔除脏数据，观察发现古文数据由text为1排列而来，而其他数据text长度不为1，因此通过判断text长度，判断是否是古文。

（3）选自文章（grade_1_2.write_article()方法）
按照.bodytext-right ::text对应的内容即为选自文章。

3.其他年级的数据处理
标题正文选自文章对应[class=chapter-three] ::text, .bodytext ::text, .bodytext-right ::text，标题和选自文章都是干净的数据，但是正文的bodytext::text还会涉及很多脏数据，那么想要把它剔除出来就需要设计一个算法
算法思路：由于古文的标题、正文、选自文章是连续的一块在所有数据之中的，所以通过判断该段内容处于标题或选自文章，来截取从古文内容，从而把想要的数据从全部的数据中取出来。
（1）判断内容是标题的方法
另外单独用.css([class=chapter-three]::text)单独获得标题的字符串数组，然后判断内容是否属于字符串数组来判断是否是标题。（标题里面有时候会含有注释标注符号，也需要通过判断是否是中文或者常用标点来进行剔除和减少换行）
（2）判断内容是选自文章的方法
由于选自文章后面都会有”》）” 或者 “改动）” 或 “改写）”的字样，所以这时候可以通过取后续两位字符进行匹配的方式，当出现这些内容了就说明内容是选自文章
（3）取出目标数据
设置布尔值isNormal，根据内容是标题或者选自文章，改写bool值，从而取出目标数据。
（4）最终结果
如图所示会在同一个txt下显示标题，正文，选自文章

七、保存数据
一二年级保存到title.txt，text.txt，article.txt三个txt文件。

三四五六年级，保存到一个txt文件中。

    with open(name + '.txt', mode='a', encoding='utf-8') as f:
        f.write(all_content)


Ps：开始是想爬取微信读书的网站，但是发现微信读书页面上的字体不是通过文本方式传输的，而是利用canvas直接用js绘制的，微信读书反爬虫做的比较好，从而选择番茄小说。
