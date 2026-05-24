# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/16 19:47
# @FileName: mutil-query.py

import dotenv
import weaviate
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
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

retriever = db.as_retriever(search_type='mmr')

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(model='deepseek-chat', temperature=0),
    include_original=True,
)

print(client.is_ready())  # Should print: `True`
docs = multi_query_retriever.invoke('关于LLM配置的文档有哪些')
print(docs)
client.close()
