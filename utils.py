#工具类
import unicodedata
import const
#如果既不是汉字也不是标点符号，返回true，是汉字或者标点符号返回False
def is_neither_chinese_nor_punctuation(char):
    # 检查是否为汉字
    if '\u4e00' <= char <= '\u9fff':  # 基本汉字
        return False
    if '\u3400' <= char <= '\u4dbf':  # 扩展A区
        return False
    if '\uf900' <= char <= '\ufaff':  # 兼容汉字
        return False
        # 这里可以添加更多的汉字Unicode范围，如果需要的话

    # 检查是否为常见的英文标点符号（这里只是示例，你可以根据需要调整）
    # 注意：这个列表并不完整，只是包含了常见的几个
    punctuation_chars = set(".,!?;:'\"()")
    if char in punctuation_chars:
        return False

        # 使用unicodedata来检查是否是其他类型的标点符号
    # 注意：这可能会误判一些你希望保留的字符
    category = unicodedata.category(char)
    if category.startswith('P'):  # 'P'开头的类别都是标点符号
        return False

        # 如果不是汉字也不是标点符号，则返回True
    return True

def text_decode(paragraph) :
    novel_content = ''
    for index in paragraph:
        try:
            word = const.dict_data[str(ord(index))]  # 尝试根据字符的Unicode码点在字典中查找映射
        except KeyError:
            word = index  # 如果查找失败，使用原始字符
        novel_content += word  # 将解码后的字符追加到章节内容中
    return novel_content
