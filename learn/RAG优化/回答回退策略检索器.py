# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/17 15:51
# @FileName: 回答回退策略检索器.py

import dotenv
import weaviate
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.init import Auth

dotenv.load_dotenv()


class StepBackRetriever(BaseRetriever):
    """回答回退检索器"""
    retriever: BaseRetriever
    llm: BaseLanguageModel

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> list[Document]:
        """构建少量提示模板"""
        examples = [
            {'input': '司机可以开快车吗？', 'output': '司机可以做什么？'},
            {'input': '程序员可以做人工智能开发吗？', 'output': '程序员可以做什么？'},
            {'input': '水果店卖西瓜吗？', 'output': '水果店卖什么？'}
        ]
        example_prompt = ChatPromptTemplate.from_messages([
            ('human', '{input}'),
            ('ai', '{output}')
        ])
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
        )

        prompt = ChatPromptTemplate.from_messages([
            ('system',
             '你是一个世界知识的专家，你的任务是回退问题，将问题改述为更一般或者前置问题，这样更容易回答，请参考示例来实现'),
            few_shot_prompt,
            ('human', '{question}')
        ])

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

step_back_retriever = StepBackRetriever(
    retriever=retriever,
    llm=ChatOpenAI(model="deepseek-chat", temperature=0)
)

documents = step_back_retriever.invoke('如何学习人工智能')
print(documents)
client.close()
