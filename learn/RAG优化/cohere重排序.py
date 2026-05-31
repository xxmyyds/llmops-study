# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/31 21:20
# @FileName: cohere重排序.py

import dotenv
import weaviate
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.init import Auth

dotenv.load_dotenv()

embedding = DashScopeEmbeddings(model='text-embedding-v4')

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

rerank = CohereRerank(model='rerank-v4.0-pro')

retriever = ContextualCompressionRetriever(
    base_retriever=db.as_retriever(search_type='mmr'),
    base_compressor=rerank
)

# retriever = db.as_retriever()
search_docs = retriever.invoke('今天晚上吃什么')
print(search_docs)
print(len(search_docs))
