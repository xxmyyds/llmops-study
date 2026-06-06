# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/2 19:28
# @FileName: gaode_weather_tool.py
import json
import os
from typing import Any, Type

import dotenv
import requests
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class GaodeWeatherArgsSchema(BaseModel):
    city: str = Field(description='需要查询天气预报的目标城市，如广州，上海')


class GaodeWeatherTool(BaseTool):
    """根据传入的城市名查询天气"""
    name: str = 'gaode_weather'
    description: str = '当你想查询天气或与天气相关的问题时可以用的工具'
    args_schema: Type[BaseModel] = GaodeWeatherArgsSchema

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        try:
            gaode_api_key = os.getenv('GAODE_API_KEY')
            if gaode_api_key is None:
                return 'no gaode api key'
            city = kwargs.get('city')
            api_domain = 'https://restapi.amap.com/v3'

            session = requests.session()

            city_response = session.request(
                method='GET',
                url=f"{api_domain}/config/district?key={gaode_api_key}&keywords={city}&subdistrict=0",
                headers={"Content-Type": "application/json; charset=utf-8"},
            )
            city_response.raise_for_status()
            city_data = city_response.json()
            if city_data.get('info') == 'OK':
                ad_code = city_data['districts'][0]['adcode']

                weather_response = session.request(
                    method='GET',
                    url=f"{api_domain}/weather/weatherInfo?key={gaode_api_key}&city={ad_code}&extensions=all&output=json",
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                if weather_data.get('info') == 'OK':
                    return json.dumps(weather_data)
            return 'get weather error'
        except Exception as e:
            return 'something error'


gaodeWeatherTool = GaodeWeatherTool()
# res = gaodeWeatherTool.invoke({'city': '上海'})
# print(res)
# print(type(res))
tools_dict = {
    gaodeWeatherTool.name: gaodeWeatherTool,
}
tools = [tool for tool in tools_dict.values()]

prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个聊天机器人，请根据用户提出的问题回答，必要时可以调用工具'),
    ('human', '{query}')
])
query = '上海天气怎么样，适合穿什么衣服'
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
