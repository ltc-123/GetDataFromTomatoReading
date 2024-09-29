import utils
import requests
import parsel

def download_books(urls, headers):
    for i in range(len(urls)):
        getData(urls[i], headers)

def getData(url, headers):
    response = requests.get(url=url, headers=headers)
    html = response.text
    # 使用parsel提取小说名称、章节标题和链接
    selector = parsel.Selector(html)
    name = selector.css('.info-name h1::text').get()  # 提取小说名称
    title_list = selector.css('.chapter-item-title::text').getall()  # 提取章节标题列表
    href = selector.css('.chapter-item-title::attr(href)').getall()  # 提取链接后缀列表
    # 调整章节链接列表，移除列表中的第一个元素，因为它不是目标章节的一部分
    href.pop(0)
    # print(href)
    # 循环提取每个章节的内容
    for title, link in zip(title_list, href):
        #当参考答案的时候跳过
        if title == "参考答案":
            continue
        link_url = 'https://fanqienovel.com' + link  # 构造完整的章节URL
        link_data = requests.get(url=link_url, headers=headers).text  # 请求章节URL并获取内容
        link_selector = parsel.Selector(link_data)
        # 可用于一二年级标题的
        content_list_title = link_selector.css("[class=chapter-three] ::text").getall()
        # 可用于一二年级的正文
        content_list_text = link_selector.css(".yinwen ruby::text, .yinwen ::text").getall()
        # 可用于一二年级的选自文章
        content_list_article = link_selector.css(".bodytext-right ::text").getall()

        write_title(content_list_title, name)
        write_text(content_list_text, name)
        write_article(content_list_article, name)

        print(title)  # 打印章节标题
        print(link_url)  # 打印章节url
def write_title(content_list_title, name):
    #标题的部分
    all_title = ''
    title_flag = True
    for paragraph in content_list_title:
        #解码段落并添加到novel_content
        novel_content = utils.text_decode(paragraph)
        if utils.is_neither_chinese_nor_punctuation(novel_content[len(novel_content) - 1]) == False:#如果是中文就正常
            if title_flag == True:
                all_title += "\n"
            else :
                title_flag = True
            all_title += novel_content
        else:
            title_flag = False
        # 保存数据
    with open(name + '_title' + '.txt', mode='a', encoding='utf-8') as f:
        f.write(all_title)
def write_text(content_list_text, name):
    #内容
    #解码章节文本，将乱码字符映射为实际字符
    all_text = ''
    last_content = ''
    temp = ''
    for paragraph in content_list_text:
        #解码段落并添加到novel_content
        novel_content = utils.text_decode(paragraph)
        if len(novel_content) > 0 and utils.is_neither_chinese_nor_punctuation(novel_content[len(novel_content) - 1]) == False:
            if len(novel_content) == 1:#属于古文里面的中文或者标点
                temp += novel_content
            elif len(novel_content) != 1 and len(last_content) == 1:#上面是古文，并把temp清零
                all_text += '\n'
                all_text += temp
                temp = ''
        last_content = novel_content
    with open(name + '_text' + '.txt', mode='a', encoding='utf-8') as f:
        f.write(all_text)
def write_article(content_list_article, name):
    # 节选自文章
    all_article = ''
    for paragraph in content_list_article:
        # 解码段落并添加到novel_content
        novel_content = utils.text_decode(paragraph)
        all_article += novel_content
        all_article += "\n"
    with open(name + '_article' + '.txt', mode='a', encoding='utf-8') as f:
        f.write(all_article)
