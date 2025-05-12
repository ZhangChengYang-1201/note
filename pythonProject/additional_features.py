import hashlib
import time
import requests
from bs4 import BeautifulSoup
import random
import re
# 广告数据库示例
ad_database = {
    'sports': ['Buy sports equipment', 'Get fit with our sports gear'],
    'technology': ['Latest gadgets available', 'Upgrade your tech today'],
    'health': ['Health insurance plans', 'Consult a doctor online']
}

def select_advertisements(query, ad_database):
    """
    根据查询选择相关广告。
    """
    ads_to_display = []
    for keyword, ads in ad_database.items():
        if keyword.lower() in query.lower():
            ads_to_display.extend(ads)
    return ads_to_display

def detect_duplicates(documents):
    """
    检测并移除重复的文档。
    """
    seen_hashes = set()
    unique_documents = []
    for doc in documents:
        doc_hash = hashlib.md5(doc.encode('utf-8')).hexdigest()
        if doc_hash not in seen_hashes:
            unique_documents.append(doc)
            seen_hashes.add(doc_hash)
    return unique_documents
#计算每个文档的MD5哈希值，哈希值相同说明重复

def remove_operators(query):
    # 定义一个正则表达式，用于匹配常见的操作符
    pattern = r'\b(AND|OR|NEAR|IN|WITHIN|AFTER|BEFORE|SINCE|UNTIL|-)'
    # 使用 re.sub 方法去掉匹配的操作符
    clean_query = re.sub(pattern, '', query, flags=re.IGNORECASE)
    # 去除多余的空格
    clean_query = ' '.join(clean_query.split())
    return clean_query

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        # 你可以添加更多 User-Agent 字符串
    ]
    return random.choice(user_agents)
#返回随机的User-Agent 字符串
def crawl_baidu(query):
    """
    根据查询词在百度上爬取信息。
    """
    query = remove_operators(query)  # 去掉查询词中的操作符
    url = "https://www.baidu.com/s"  # 定义百度搜索的基本 URL
    params = {'wd': query}  # 将查询词作为 URL 参数传递，'wd' 是百度搜索的查询参数
    headers = {'User-Agent': get_random_user_agent()}  # 使用随机的 User-Agent 字符串创建请求头

    try:
        response = requests.get(url, params=params, headers=headers)  # 发送 HTTP GET 请求
        response.raise_for_status()  # 检查请求是否成功，如果不成功则抛出异常
    except requests.RequestException as e:
        print(f"请求失败：{e}")  # 如果请求失败，打印错误信息
        return []  # 返回空列表

    try:
        soup = BeautifulSoup(response.text, 'html.parser')  # 解析返回的 HTML 内容
        results = []  # 初始化一个空列表用于存储搜索结果
        for result in soup.find_all('div', {'class': 'c-container'}):  # 查找所有包含搜索结果的 div 元素
            title = result.find('a')  # 查找结果中的第一个 a 标签，通常是标题
            snippet = result.find('div', {'class': 'c-abstract'})  # 查找结果中的摘要 div 元素
            results.append({
                'title': title.text.strip() if title else "No title",  # 如果找到标题，则去除两端的空白字符，否则返回 "No title"
                'snippet': snippet.text.strip() if snippet else "No snippet",  # 如果找到摘要，则去除两端的空白字符，否则返回 "No snippet"
                'link': title['href'] if title else "No link"  # 如果找到标题，则获取其链接，否则返回 "No link"
            })
    except Exception as e:
        print(f"解析错误: {e}")  # 如果解析 HTML 过程中出现错误，打印错误信息
        return []  # 返回空列表

    # 添加随机延迟，减少爬虫行为的可检测性
    time.sleep(random.uniform(1, 3))
    return results  # 返回搜索结果列表
