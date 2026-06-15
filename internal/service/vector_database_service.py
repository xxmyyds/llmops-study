# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/4 11:05
# @FileName: vector_database_service.py

import os

import weaviate
from injector import inject
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient
from weaviate.classes.init import Auth


@inject
class VectorDatabaseService:
    """向量数据库服务"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        """构造函数，完成向量数据库服务的客户端+LangChain向量数据库实例的创建"""
        # 1.创建/连接weaviate向量数据库
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url='owz5xuu6rckr2opo8ewwlw.c0.asia-southeast1.gcp.weaviate.cloud',
            auth_credentials=Auth.api_key(
                'Z0FwS0JlT0Z5VlZaaHV4OF9mNUkvd2FUU1hGNUFxQXhRdEtFZjJxR213U1FCY3Ixdm9kQkE3Qld3SFd3PV92MjAw'),
            skip_init_checks=True
        )

        # 2.创建LangChain向量数据库

        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="llmops",
            text_key="text",
            embedding=DashScopeEmbeddings(
                model='text-embedding-v4',
                dashscope_api_key=os.environ['DASHSCOPE_API_KEY'],
            )
        )

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        """将对应的文档列表使用换行符进行合并"""
        return "\n\n".join([document.page_content for document in documents])
