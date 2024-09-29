import utils
import requests
import parsel
def download_books(urls, headers):
    for i in range(len(urls)):
        getData(urls[i], headers)

def getData(url, headers):
    response = requests.get(url, headers=headers)
    html = response.text
    #使用parsel提取小说名称、章节标题和链接
    selector = parsel.Selector(html)
    name = selector.css('.info-name h1::text').get()  # 提取小说名称
    title_list = selector.css('.chapter-item-title::text').getall()  # 提取章节标题列表
    href = selector.css('.chapter-item-title::attr(href)').getall()  # 提取链接后缀列表
    # 调整章节链接列表，移除列表中的第一个元素，因为它不是目标章节的一部分
    href.pop(0)
    # 循环提取每个章节的内容
    for title, link in zip(title_list, href):
        if title == "参考答案":
            continue
        link_url = 'https://fanqienovel.com' + link  # 构造完整的章节URL
        link_data = requests.get(url=link_url, headers=headers).text  # 请求章节URL并获取内容
        link_selector = parsel.Selector(link_data)
        #可用于三四五六年级的标题正文选自
        content_list2 = link_selector.css("[class=chapter-three] ::text").getall()
        content_list3 = link_selector.css("[class=chapter-three] ::text, .bodytext ::text, .bodytext-right ::text").getall()

        write_content(content_list2, content_list3, name)

        print(title)  # 打印章节标题
        print(link_url)  # 打印章节url
#写入内容
def write_content(content_list2, content_list3, name):
    isNormal = False
    is_title_and_isquan = False
    all_title = []
    #先找出标题
    for paragraph in content_list2:
        #解码段落并添加到novel_content
        novel_content = utils.text_decode(paragraph)
        all_title.append(novel_content)

    all_content = ''
    for paragraph in content_list3:
        # 解码段落并添加到novel_content
        novel_content = utils.text_decode(paragraph)
        #如果是标题的话,设置为正文模式，后面isNormal自然会把标题加进去
        if len(novel_content) > 0 and novel_content in all_title:
            #标题首字母不是汉字而是圈的话,设置is_title_and_isquan为true
            if utils.is_neither_chinese_nor_punctuation(novel_content[0]) and isNormal == True:
                is_title_and_isquan = True
            isNormal = True
        #如果是选自的话，设置为非正文模式
        if len(novel_content) > 1 and novel_content[len(novel_content) - 1] == '）' and (novel_content[len(novel_content) - 2] == '》' or novel_content[len(novel_content) - 2] == '动'or novel_content[len(novel_content) - 2] == '写'):
            #选自上面的\n也要撤销
            all_content = all_content[:-1]
            all_content += novel_content
            all_content += '\n'
            isNormal = False
        #剩下的内容只有在isNormal是True，即正文模式的时候才处理
        if isNormal:
            #如果是标题的圈的话，去掉首个并且去点之前的\n
            if is_title_and_isquan:
                novel_content = novel_content[1:]
                all_content = all_content[:-1]
                all_content += novel_content
                all_content += '\n'
                is_title_and_isquan = False
            #是汉字或者标点符号的的话才处理，圈不处理
            elif len(novel_content) > 0 and utils.is_neither_chinese_nor_punctuation(novel_content[len(novel_content) - 1]) == False:
                all_content += novel_content
                all_content += '\n'
            elif len(novel_content) > 0:#是圈,把前面的换行符去掉
                all_content =  all_content[:-1]

    # 写入文件，并保存爬取内容
    with open(name + '.txt', mode='a', encoding='utf-8') as f:
        f.write(all_content)
