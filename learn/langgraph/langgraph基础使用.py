# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/10 20:06
# @FileName: langgraph基础使用.py
from typing import TypedDict, Annotated

import dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

dotenv.load_dotenv()

llm = ChatOpenAI(model='gpt-4o')


# 创建状态图
class State(TypedDict):
    """图结构的状态数据"""
    messages: Annotated[list, add_messages]
    use_name: str


def chatbot(state: State):
    """聊天机器人节点，使用大语言模型根据传递的消息列表生成内容"""
    ai_message = llm.invoke(state['messages'])
    return {'messages': [ai_message], 'use_name': state['use_name']}


graph_builder = StateGraph(State)

# 添加节点
graph_builder.add_node('llm', chatbot)

# 添加边
# graph_builder.set_entry_point('llm')
# graph_builder.set_finish_point('llm')
graph_builder.add_edge(START, 'llm')
graph_builder.add_edge('llm', END)

# 编译图为Runnable可运行组件
graph = graph_builder.compile()

# 调用
res = graph.invoke(
    {
        "messages": [
            ('human', '你好你是什么大模型')
        ],
        "use_name": "user"
    }
)
print(res)
