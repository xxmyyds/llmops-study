# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/17 11:41
# @FileName: 多结果查询融合.py
from typing import Any

import dotenv
import weaviate
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.load import dumps, loads
from langchain_openai import ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.init import Auth

dotenv.load_dotenv()


def rrf(results: list[list], k: int = 60) -> list[tuple[Any, Any]]:
    """rrf算法,对传递的二层嵌套文档列表进行去重合并，并返回排名高的数据"""
    fused_result = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            """使用dumps函数将类实例转化成字符串"""
            doc_str = dumps(doc)
            if doc_str not in fused_result:
                fused_result[doc_str] = 0
            fused_result[doc_str] += 1 / (rank + k)
    reranked_result = [
        (loads(doc), score)
        for doc, score in sorted(fused_result.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked_result


class RAGFusionRetriever(MultiQueryRetriever):
    """RAG多查询结果融合策略检索器"""
    k: int = 4

    def retrieve_documents(
            self,
            queries: list[str],
            run_manager: CallbackManagerForRetrieverRun,
    ) -> list[list]:
        documents = []
        for query in queries:
            docs = self.retriever.invoke(query, config={"callbacks": run_manager.get_child()})
            documents.append(docs)
        return documents

    def unique_union(self, documents: list[Document]) -> list[Document]:
        """rrf算法,对传递的二层嵌套文档列表进行去重合并，并返回排名高的数据"""
        fused_result = {}

        for docs in documents:
            for rank, doc in enumerate(docs):
                """使用dumps函数将类实例转化成字符串"""
                doc_str = dumps(doc)
                if doc_str not in fused_result:
                    fused_result[doc_str] = 0
                fused_result[doc_str] += 1 / (rank + 60)
        reranked_result = [
            (loads(doc), score)
            for doc, score in sorted(fused_result.items(), key=lambda x: x[1], reverse=True)
        ]
        return [item[0] for item in reranked_result[:self.k]]


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

rag_fusion_retriever = RAGFusionRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(model='deepseek-chat', temperature=0),
    include_original=True,
)

docs = rag_fusion_retriever.invoke('关于LLM配置的文档有哪些')
print(docs)
client.close()
