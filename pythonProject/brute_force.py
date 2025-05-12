import os
import re

def read_documents(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding='utf-8') as file:
                doc_id = filename
                content = file.read()
                content = content.lower()
                content = re.sub(r'[^a-z\s]', '', content)
                words = re.findall(r'\b[a-z]+\b', content)
                documents[doc_id] = words
    return documents
    #字典形式返回文件名和对应的单词列表。


def brute_force_boolean_search(query, documents):
    # 将查询字符串转换为小写并按空格分割
    query = query.lower().split()
    # 初始化结果集为所有文档
    result_docs = set(documents.keys())

    # 遍历查询中的每个词
    i = 0
    while i < len(query):
        term = query[i]
        if term == 'and':
            # AND 运算符，需要找到包含AND后面词的所有文档
            next_term = query[i + 1]
            result_docs &= set(doc for doc, words in documents.items() if next_term in words)
            i += 1  # 跳过处理AND后面的词
        elif term == 'or':
            # OR 运算符，需要找到包含OR后面任意词的所有文档
            next_term = query[i + 1]
            result_docs |= set(doc for doc, words in documents.items() if next_term in words)
            i += 1  # 跳过处理OR后面的词
        elif term == 'not':
            # NOT 运算符，需要排除包含NOT后面词的所有文档
            next_term = query[i + 1]
            result_docs -= set(doc for doc, words in documents.items() if next_term in words)
            i += 1  # 跳过处理NOT后面的词
        else:
            # 如果是普通词，则找到包含该词的所有文档
            result_docs &= set(doc for doc, words in documents.items() if term in words)
        i += 1

    return list(result_docs)



