import math
from collections import defaultdict, Counter
import numpy as np



def pagerank(M, num_iterations: int = 100, d: float = 0.85):
    N = M.shape[1]
    v = np.random.rand(N, 1)
    v = v / np.linalg.norm(v, 1)
    teleport = (1 - d) / N
    for i in range(num_iterations):
        v = d * np.matmul(M, v) + teleport
    return v

# 假设我们有一个NxN的矩阵M，其中如果文档j链接到文档i，则M[i][j] = 1 / L[j]，L[j]是文档j的外链数量。

def compute_tf(document):
    tf_dict = {}
    total_terms = len(document)
    term_count = Counter(document)

    for term, count in term_count.items():
        tf_dict[term] = count / total_terms
    return tf_dict


def compute_idf(documents):
    idf_dict = {}
    total_documents = len(documents)
    term_document_counts = defaultdict(int)

    for document in documents:
        for term in set(document):
            term_document_counts[term] += 1

    for term, count in term_document_counts.items():
        idf_dict[term] = math.log(total_documents / (1 + count))
    return idf_dict


def compute_tf_idf(documents):
    document_tfs = [compute_tf(doc) for doc in documents]
    idf = compute_idf(documents)
    tf_idfs = []

    for tf in document_tfs:
        doc_tf_idf = {term: tf[term] * idf[term] for term in tf}
        tf_idfs.append(doc_tf_idf)
    return tf_idfs


def cosine_similarity(query_tf_idf, document_tf_idf):
    # 转换为NumPy数组
    query_vec = np.array([query_tf_idf.get(term, 0) for term in query_tf_idf])
    doc_vec = np.array([document_tf_idf.get(term, 0) for term in query_tf_idf])

    # 计算点积
    numerator = np.dot(query_vec, doc_vec)

    # 计算模长
    norm_query = np.linalg.norm(query_vec)
    norm_doc = np.linalg.norm(doc_vec)

    # 防止除以零
    if norm_query == 0 or norm_doc == 0:
        return 0.0

    # 计算余弦相似度
    return float(numerator) / (norm_query * norm_doc)


def rank_documents(query, documents, doc_pagerank_scores):
    query = query.split()
    document_tfs = [compute_tf(doc_content) for doc_content, _, _ in documents]
    idf = compute_idf([doc_content for doc_content, _, _ in documents])
    query_tf = compute_tf(query)
    query_tf_idf = {term: query_tf[term] * idf.get(term, 0) for term in query_tf}

    scores = []
    for (_, doc_name, _), doc_tf in zip(documents, document_tfs):
        doc_tf_idf = {term: doc_tf[term] * idf.get(term, 0) for term in doc_tf}
        similarity = cosine_similarity(query_tf_idf, doc_tf_idf)
        pagerank_score = doc_pagerank_scores.get(doc_name, 0)
        combined_score = similarity * 0.7 + pagerank_score * 0.3  # PageRank得分占30%
        scores.append((combined_score, doc_name))

    return sorted(scores, reverse=True, key=lambda x: x[0])

"""
import os
import re
import networkx as nx
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 确保下载了所需的 NLTK 资源
nltk.download('punkt')

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

def read_documents(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding='utf-8') as file:
                doc_id = filename
                content = file.read().lower()
                content = re.sub(r'[^a-z\s]', '', content)
                words = nltk.word_tokenize(content)  # Tokenize document content
                documents[doc_id] = words
    return documents

def build_document_graph(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(words) for words in documents.values()])
    cosine_sim = cosine_similarity(tfidf_matrix)

    graph = nx.Graph()
    doc_names = list(documents.keys())
    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            if cosine_sim[i][j] > 0.1:  # Using 0.1 as similarity threshold
                graph.add_edge(doc_names[i], doc_names[j], weight=cosine_sim[i][j])
    return graph

def compute_pagerank(graph):
    return nx.pagerank(graph, weight='weight')

def compute_tf_idf(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(words) for words in documents.values()])
    tfidf_dict = {doc_id: tfidf_matrix[i] for i, doc_id in enumerate(documents.keys())}
    return vectorizer, tfidf_dict
def read_and_compute_pagerank(folder_path):
    # Building a graph of document relationships based on cosine similarity
    def build_document_graph(documents):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([" ".join(words) for words in documents.values()])
        cosine_sim = cosine_similarity(tfidf_matrix)

        graph = nx.Graph()
        doc_names = list(documents.keys())
        for i in range(len(doc_names)):
            for j in range(i + 1, len(doc_names)):
                if cosine_sim[i][j] > 0.1:  # Using 0.1 as similarity threshold
                    graph.add_edge(doc_names[i], doc_names[j], weight=cosine_sim[i][j])
        return graph

    # Calculating PageRank scores from the graph
    def compute_pagerank(graph):
        return nx.pagerank(graph, weight='weight')

    documents = read_documents(folder_path)
    document_graph = build_document_graph(documents)
    pagerank_scores = compute_pagerank(document_graph)

    return documents, pagerank_scores
def rank_documents(query, documents, pagerank_scores, vectorizer, tfidf_dict):
    query = query.lower()
    query = re.sub(r'[^a-z\s]', '', query)
    query_words = nltk.word_tokenize(query)
    query_vector = vectorizer.transform([" ".join(query_words)])

    scores = []
    for doc_id, tfidf_vector in tfidf_dict.items():
        similarity = cosine_similarity(query_vector, tfidf_vector)[0][0]
        pagerank_score = pagerank_scores.get(doc_id, 0)
        combined_score = similarity * 0.7 + pagerank_score * 0.3  # PageRank score占30%
        scores.append((combined_score, doc_id))

    return sorted(scores, reverse=True, key=lambda x: x[0])
"""


