# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/3 16:39
# @FileName: HuggingFace.py
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L12-V2',
    cache_folder='./embeddings/',
)
query_vector = embeddings.embed_query('你好我是xxm')
print(query_vector)
print(len(query_vector))
