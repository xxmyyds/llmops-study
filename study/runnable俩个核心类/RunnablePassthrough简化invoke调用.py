# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/18 15:50
# @FileName: RunnablePassthrough简化invoke调用.py
# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/18 11:32
# @FileName: RunnableParallel模拟检索.py

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    print('正在检索:', query)
    return '我是Bob'


prompt = ChatPromptTemplate.from_template("""请根据用户的问题回答,可以参考对应的上下文进行生成

<context>
{context}
</context>

用户的问题是: {query}
""")

llm = ChatOpenAI(model='deepseek-chat')
parser = StrOutputParser()
chain = {
            'context': retrieval,
            'query': RunnablePassthrough()
        } | prompt | llm | parser

content = chain.invoke('你好, 我是谁')

# chain = RunnablePassthrough.assign(context=lambda x: retrieval(x['query'])) | prompt | llm | parser
#
# content = chain.invoke({'query': '你好, 我是谁'})
print(content)
