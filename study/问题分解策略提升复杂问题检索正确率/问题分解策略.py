# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/17 13:35
# @FileName: 问题分解策略.py
from operator import itemgetter

import dotenv
import weaviate
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.init import Auth

dotenv.load_dotenv()


def format_qa_pairs(question: str, answer: str) -> str:
    """格式化传递的问题+答案为单个的字符串"""
    return f"Question: {question}\nAnswer: {answer}\n\n".strip()


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

decomposition_prompt = ChatPromptTemplate.from_template(
    "你是一个乐于助人的AI助手，可以针对一个输入问题生成多个相关的子问题。\n"
    "目标是将输入问题分解成一组可以独立回答的子问题或子任务。\n"
    "生成与以下问题相关的多个搜索查询：{question}\n"
    "并使用换行符进行分割，输出(3个子问题/子查询)："
)

decomposition_chain = (
        {'question': RunnablePassthrough()}
        | decomposition_prompt
        | ChatOpenAI(model='deepseek-chat', temperature=0)
        | StrOutputParser()
        | (lambda x: x.strip().split('\n'))
)

question = '如何学习人工智能'
sub_questions = decomposition_chain.invoke(question)

prompt = ChatPromptTemplate.from_template("""这是你需要回答的问题:
---
{question}
---

这是所有可用的背景问题和答案对：
---
{qa_pairs}
---

这是与问题相关的额外背景信息
---
{context}
---"""
                                          )
chain = (
        {
            'question': itemgetter('question'),
            'qa_pairs': itemgetter('qa_pairs'),
            'context': itemgetter('question') | retriever,
        }
        | prompt
        | ChatOpenAI(model='deepseek-chat', temperature=0)
        | StrOutputParser()
)
qa_pairs = ''
for sub_question in sub_questions:
    answer = chain.invoke({'question': sub_question, 'qa_pairs': qa_pairs})
    qa_pair = format_qa_pairs(question=sub_question, answer=answer)
    qa_pairs += "\n----\n" + qa_pair
    print(f"问题：{sub_question}")
    print(f"答案：{answer}")

client.close()
