import os
import re
from collections import Counter, defaultdict

# 创建倒排索引
def create_inverted_index(path):
    index = defaultdict(list)
    files = os.listdir(path)  # 获取目录下的所有文件
    for file in files:
        if not os.path.isdir(file):
            file_path = os.path.join(path, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()  # 转换为小写
            words = re.sub(r"[^\w\s]", " ", content).split()  # 去除标点并分词
            dic_word_count = Counter(words)  # 计算词频

            for word, count in dic_word_count.items():
                index[word].append([file, count])
    return index

def write_inverted_index_to_file(index, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, file_list in index.items():
            f.write(f"{word}: {file_list}\n")

def save_inverted_index_to_txt(index, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for word, occurrences in index.items():
            # 格式化输出每个单词及其在各个文件中的出现次数
            f.write(f"{word}:\n")
            for occurrence in occurrences:
                f.write(f"\t{occurrence[0]}: {occurrence[1]} times\n")
            f.write("\n")  # 在每个单词条目之后添加空行以提高可读性
# 解析和执行查询
def process_query(index, query):
    query_elements = re.split(r'\s+', query.lower())
    initial_results = set(os.listdir("D:/信息检索/语料2"))  # 初始化所有文件的集合

    current_operator = "AND"  # 默认操作符
    current_results = set(initial_results)
    pending_negations = set()

    for element in query_elements:
        if element.upper() == "AND":
            current_operator = "AND"
        elif element.upper() == "OR":
            current_operator = "OR"
        elif element.upper() == "NOT":
            current_operator = "NOT"
        else:
            if element in index:
                doc_set = {doc_info[0] for doc_info in index[element]}
                if current_operator == "AND":
                    current_results.intersection_update(doc_set)
                elif current_operator == "OR":
                    current_results.update(doc_set)
                elif current_operator == "NOT":
                    if pending_negations:
                        pending_negations.intersection_update(doc_set)
                    else:
                        pending_negations = set(initial_results).intersection(doc_set)
            else:
                if current_operator == "AND":
                    current_results.clear()  # 如果AND操作的词不在索引中，结果为空
                elif current_operator == "NOT":
                    # 对于 NOT 操作符，如果词不在索引中，相当于没有这个词，不进行操作
                    continue

    # 应用所有的否定
    current_results.difference_update(pending_negations)

    return current_results
#查找符合条件的文档集合

path_to_documents = 'D:/信息检索/语料2'  # 修改为实际文档路径
output_file = 'inverted_index2.txt'
index = create_inverted_index(path_to_documents)
write_inverted_index_to_file(index, output_file)
print(f"Inverted index has been written to {output_file}")
