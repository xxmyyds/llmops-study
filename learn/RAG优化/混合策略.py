# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/17 21:39
# @FileName: 混合策略.py
import dotenv
import weaviate
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.init import Auth

dotenv.load_dotenv()


class HyDERetriever(BaseRetriever):
    """混合检索器"""
    retriever: BaseRetriever
    llm: BaseLanguageModel

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> list[Document]:
        prompt = ChatPromptTemplate.from_template(
            "请写一篇科学论文来回答这个问题\n"
            "问题：{question}\n"
            "文章："
        )

        chain = (
                {'question': RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
                | self.retriever
        )

        return chain.invoke(query)


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

hyde_retriever = HyDERetriever(
    retriever=retriever,
    llm=ChatOpenAI(model="deepseek-chat", temperature=0)
)

documents = hyde_retriever.invoke('如何学习人工智能')
print(documents)
client.close()
