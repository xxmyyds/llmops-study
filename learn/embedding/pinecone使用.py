# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/3 18:53
# @FileName: pinecone使用.py
import dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_pinecone import PineconeVectorStore

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
    {'page': 4, 'id': 1},
    {'page': 5},
    {'page': 6},
    {'page': 7},
    {'page': 8},
    {'page': 9},
    {'page': 10},
    {'page': 11}
]

db = PineconeVectorStore(index_name='llmops', embedding=embedding, namespace='dataset')
# db.add_texts(texts, metadatas, namespace='dataset')
query = '我喜欢人工智能'

print(db.similarity_search_with_relevance_scores(
    query,
    # filter={'page': {'$lte': 5}}
    filter={'$and': [{'page': 4}, {'id': 1}]}
))
pinecone_index = db.get_pinecone_index('llmops')

print(pinecone_index)
