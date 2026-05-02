# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/2 18:22
# @FileName: embedding使用.py
import dotenv
import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings
from numpy.linalg import norm

dotenv.load_dotenv()


def cosine_similarity(vec1: list, vec2: list) -> float:
    """计算传入的俩个向量的余弦相似度,值越大相似度越大"""
    """点积"""
    do_product = np.dot(vec1, vec2)

    """计算向量的长度"""
    vec1_norm = norm(vec1)
    vec2_norm = norm(vec2)

    return do_product / (vec1_norm * vec2_norm)


embeddings = DashScopeEmbeddings(model='text-embedding-v4')
query_vector = embeddings.embed_documents([
    '我是xxm,我喜欢看电影',
    '我喜欢看电影，我叫xxm',
    '今天是个好天气'
])
print(len(query_vector))
print(cosine_similarity(query_vector[0], query_vector[1]))
print(cosine_similarity(query_vector[1], query_vector[2]))
