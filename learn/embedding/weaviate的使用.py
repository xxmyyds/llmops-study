# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/3 21:11
# @FileName: weaviate的使用.py
import dotenv
import weaviate
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.init import Auth
from weaviate.classes.query import Filter

dotenv.load_dotenv()

embedding = DashScopeEmbeddings(model='text-embedding-v4')

texts = [
    # 1. 基础语义对比
    "我爱自然语言处理技术",
    "我喜欢用Python做数据分析",
    "今天北京的天气真好",

    # 2. 相似语义（用于测试相似度）
    "机器学习是人工智能的一个分支",
    "深度学习属于机器学习的重要领域",
    "AI技术中的神经网络非常强大",

    # 3. 差异明显的文本
    "向量数据库用于存储和检索高维向量",
    "今天中午吃什么好呢",
    "特斯拉的股价昨天大涨5%",

    # 4. 长文本示例（测试性能）
    "检索增强生成（RAG）是一种结合了信息检索和大语言模型的技术架构。"
    "它首先从知识库中检索相关文档片段，然后将这些片段作为上下文输入给大模型，"
    "让模型基于真实数据生成更准确、更可靠的回答，有效减少幻觉问题。",

    # 5. 技术文档片段
    "DashScope是阿里云提供的模型服务平台，集成了通义千问、Embedding、"
    "语音识别等多种AI能力，开发者可以通过统一的API调用这些服务。"
]
metadatas = [
    {'page': 1},
    {'page': 2},
    {'page': 3},
    {'page': 4, 'account_id': 1},
    {'page': 5},
    {'page': 6},
    {'page': 7},
    {'page': 8},
    {'page': 9},
    {'page': 10},
    {'page': 11}
]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url='6aypz6aysys4h4jfym0lg.c0.asia-southeast1.gcp.weaviate.cloud',
    auth_credentials=Auth.api_key(
        'eGJBVU1CSm8rYm55cTByS18xL1JVK0xBL2Z6OUpEb0R5VEpDdmZ3R054VWd1UDR3VitZbzNzNjFWdG9ZPV92MjAw')
)
db = WeaviateVectorStore(
    client=client,
    index_name='DatasetDemo',
    text_key='text',
    embedding=embedding,
)

# ids = db.add_texts(texts, metadatas)
# print(ids)
# print(len(ids))

print(client.is_ready())  # Should print: `True`
filters = Filter.by_property('page').greater_or_equal(5)
print(db.similarity_search_with_score(
    '我喜欢人工智能',
    filters=filters
))
client.close()
