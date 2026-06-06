# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/2 20:54
# @FileName: google_serper_tool.py

import dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description='执行谷歌搜索的查询语句')


google_serper = GoogleSerperRun(
    name='GoogleSerper',
    description='Google Search',
    api_wrapper=GoogleSerperAPIWrapper(),
)
# print(google_serper.invoke('vue 的作者是谁'))
tools_dict = {
    google_serper.name: google_serper,
}
tools = [tool for tool in tools_dict.values()]

prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个聊天机器人，请根据用户提出的问题回答，必要时可以调用工具'),
    ('human', '{query}')
])
query = '帮我搜索下上海天气怎么样，适合穿什么衣服'
llm = ChatOpenAI(model='deepseek-chat', temperature=0)
llm_with_tool = llm.bind_tools(tools=tools)

chain = {"query": RunnablePassthrough()} | prompt | llm_with_tool

res = chain.invoke(query)
tool_calls = res.tool_calls
if len(tool_calls) <= 0:
    print(res.content)
else:
    messages = prompt.invoke(query).to_messages()
    messages.append(res)

    for tool_call in tool_calls:
        tool = tools_dict.get(tool_call.get('name'))
        content = tool.invoke(tool_call.get('args'))
        tool_call_id = tool_call.get('id')
        messages.append(ToolMessage(tool_call_id=tool_call_id, content=content))

    print('输出内容：', llm_with_tool.invoke(messages))
