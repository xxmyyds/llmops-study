# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/26 15:16
# @FileName: 缓冲窗口记忆.py
from operator import itemgetter

import dotenv
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个智能的聊天机器人,需要根据用户的问题和上下文来回答问题'),
    MessagesPlaceholder('history'),
    ('human', '{query}'),
])
memory = ConversationBufferWindowMemory(k=2, return_messages=True, input_key='query')

llm = ChatOpenAI(model='deepseek-v4-flash')

chain = RunnablePassthrough.assign(
    history=RunnableLambda(memory.load_memory_variables) | itemgetter('history'),
) | prompt | llm | StrOutputParser()

while True:
    query = input("Human: ")

    if query == 'quit' or query == 'q':
        exit(0)

    chain_input = {'query': query, 'history': []}

    print('AI: ')
    response = chain.stream(chain_input)
    output = ''
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end='')
    memory.save_context(chain_input, {'output': output})
    print("")
    print('history: ', memory.load_memory_variables({}))
