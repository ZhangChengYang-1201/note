import numpy as np
import os
import re
from DaoPaiSuoYin import create_inverted_index, save_inverted_index_to_txt, process_query
from brute_force import read_documents, brute_force_boolean_search
from text_search import compute_tf, rank_documents, compute_idf, compute_tf_idf, cosine_similarity
from query_expansionANDsummery import fuzzy_match, sentence
from additional_features import select_advertisements, detect_duplicates, crawl_baidu

def read_documentss(folder_path):
    filename_to_document = {}
    doc_authority_scores = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # 假设所有文档都是文本文件
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                filename_to_document[filename] = content
                doc_authority_scores[filename] = np.random.random()  # 这里应使用实际计算的PageRank得分
    return filename_to_document, doc_authority_scores


def main():
    folder_path = "D:/信息检索/语料2"

    # 从终端读取用户输入的 query、key 和 fuzzy_keys
    query = input("请输入查询词: ")
    keys_input = input("请输入用于句子提取的关键词（用逗号分隔）: ")
    keys = [key.strip() for key in keys_input.split(',')]
    fuzzy_keys_input = input("请输入需要模糊匹配的多个词（用逗号分隔）: ")
    fuzzy_keys = [key.strip() for key in fuzzy_keys_input.split(',')]

    # 使用 DaoPaiSuoYin 模块
    index = create_inverted_index(folder_path)
    results_dps = process_query(index, query)
    print("使用倒排索引匹配的文件:", results_dps)

    # 读取文档并获取文档内容和权威性得分
    filename_to_document, doc_authority_scores = read_documentss(folder_path)

    documents = read_documents(folder_path)
    results_bf = brute_force_boolean_search(query, documents)
    print("使用暴力搜索匹配的文件:", results_bf)

    # 过滤文档：使用文件名直接索引文档内容
    filtered_documents = [(filename_to_document[filename], filename, doc_authority_scores[filename])
                          for filename in results_dps if filename in filename_to_document]

    # 对过滤后的文档进行排名
    ranked_documents = rank_documents(query, filtered_documents, doc_authority_scores)

    # 打印排名结果
    for score, doc_name in ranked_documents:
        print(f"Score: {score:.4f}, Document: {doc_name}")

    # 使用 sentence 函数提取包含关键词的句子
    file_list = list(filename_to_document.keys())
    print("\n包含关键词的句子:")
    for key in keys:
        sentence(file_list, [file_list.index(doc_name) + 1 for _, doc_name in ranked_documents], key)

    # 初始化一个集合存放所有匹配结果
    combined_fuzzy_results = set()

    # 对每个词单独进行模糊匹配并合并结果
    for key in fuzzy_keys:
        fuzzy_results = fuzzy_match(key)
        combined_fuzzy_results.update(fuzzy_results)

    # 打印查询拓展结果
    print("\n查询拓展结果:")
    for res in combined_fuzzy_results:
        print(res)

    ad_database = {
        "电影": ["看最新电影请访问xxx网站"],
        "书籍": ["优惠书籍在此！"],
    }

    # 重复检测
    unique_results = detect_duplicates([doc[1] for doc in ranked_documents])
    print("\n无重复的搜索结果:", unique_results)

    # 打印爬取结果和广告
    print("搜索结果：")
    for res in unique_results:
        print(res)

    # 选择相关广告
    ads = select_advertisements(query, ad_database)

    print("\n广告：")
    for ad in ads:
        print(ad)

    # 爬取百度搜索结果
    baidu_results = crawl_baidu(query)
    print("\n百度搜索结果:")
    for result in baidu_results:
        print(result['title'], result['link'])


if __name__ == '__main__':
    main()