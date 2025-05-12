import re
import os
import re

def sentence(files, li, key):  # 输出关键词所在句子
    j = 0
    for i in li:
        if j >= 6:
            break
        name = files[i - 1]
        print(name)
        pathname = os.path.join('D:/信息检索/语料2', name)  # 使用 os.path.join 构建路径
        try:
            with open(pathname, 'r', encoding='utf-8') as text:
                for line in text:
                    # 构建匹配句子的正则表达式
                    pattern = re.compile(r'[^.?!\u3000]*[.?!]*[^.?!\u3000]*' + re.escape(key) + r'[^.?!\u3000]*[.?!][^.?!\u3000\n]*')
                    search = re.findall(pattern, line)
                    if search:
                        for sentence in search:
                            print(sentence)
        except FileNotFoundError:
            print(f"文件 {pathname} 未找到")
        except Exception as e:
            print(f"处理文件 {pathname} 时发生错误: {e}")
        j += 1
        print()

def fuzzy_match(key):  # 模糊匹配，返回满足通配符条件的词
    if1 = 0
    if '*' not in key:
        key += '*'
    key += '\n'  # 修正拼接错误
    j = 0
    if key[0] == '*':
        key = key[1:]
    elif key[-2] == '*':
        if1 = 1
        for i in range(len(key)):
            if key[i] == '*':
                j = i  # 记录*位置
                key = key[:j]
                break
    else:
        for i in range(len(key)):
            if key[i] == '*':
                j = i  # 记录*位置
                key = key[j + 1:] + key[:j]
                break
    res = []  # 存放所有满足通配查询的词
    with open('../IR/homework/Permuterm Index.txt', 'r', encoding='utf-8') as f:
        for line in f:
            li = line.split(' ')
            i = 1
            while i < len(li):
                if key == li[i][:len(key)]:
                    if if1 == 1 and ')' in li[i]:
                        suffix = li[i].split(')', 1)
                        if len(suffix) > 1 and suffix[1] != '':
                            break
                    res.append(li[0])
                    break
                i += 1
    return res

def score(tf_idf_scores):  # 根据tf-idf评分 降序输出
    sorted_items = sorted(tf_idf_scores.items(), key=lambda d: d[1], reverse=True)  # 根据分数降序排序
    sorted_document_ids = [doc_id for doc_id, score in sorted_items]  # 提取文档ID列表
    return sorted_document_ids