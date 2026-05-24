# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/4 09:12
# @FileName: 手写自定义向量数据库.py
import uuid
from typing import Any

import dotenv
import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

dotenv.load_dotenv()


class MemoryVectorStore(VectorStore):
    """基于内存+欧几里得距离的向量数据库"""
    store: dict = {}

    def add_texts(
            self,
            texts: list[str],
            metadatas: list[dict] | None = None,
            *,
            ids: list[str] | None = None,
            **kwargs: Any,
    ) -> list[str] | None:
        if metadatas is not None and len(metadatas) != len(texts):
            raise ValueError('metadatas解析错误')

        embeddings = self._embeddings.embed_documents(texts)
        ids = [str(uuid.uuid4()) for _ in texts]

        for idx, text in enumerate(texts):
            self.store[ids[idx]] = {
                'id': ids[idx],
                'text': text,
                'vector': embeddings[idx],
                'metadatas': metadatas[idx] if metadatas is not None else {}
            }

        return ids

    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> list[Document]:
        embeddings = self._embeddings.embed_query(query)
        results = []
        for key, record in self.store.items():
            distance = self._euclidean_distance(embeddings, record['vector'])
            results.append({'distance': distance, **record})

        # 排序
        sorted_results = sorted(results, key=lambda x: x['distance'])

        results_k = sorted_results[:k]

        return [
            Document(page_content=item['text'], metadatas={**item['metadatas'], 'score': item['distance']})
            for item in results_k
        ]

    @classmethod
    def from_texts(cls: type['MemoryVectorStore'], texts: list[str], embeddings: Embeddings,
                   metadatas: list[dict] | None = None, *,
                   ids: list[str] | None = None, **kwargs: Any) -> 'MemoryVectorStore':
        memory_vector_store = cls(embeddings=embeddings)
        memory_vector_store.add_texts(texts, metadatas=metadatas, **kwargs)
        return memory_vector_store

    @classmethod
    def _euclidean_distance(cls, vec1: list, vec2: list) -> float:
        """计算俩个向量的欧几里得距离"""
        return np.linalg.norm(np.array(vec1) - np.array(vec2))

    def __init__(self, embeddings: Embeddings):
        self._embeddings = embeddings


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

db = MemoryVectorStore(embeddings=embedding)
ids = db.add_texts(texts, metadatas=metadatas)
print(ids)
