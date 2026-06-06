# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/6 11:53
# @FileName: 不支持函数调用的方式.py
import json
import os
from typing import Any, Type, Optional, Dict, TypedDict

import dotenv
import requests
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, RunnablePassthrough
from langchain_core.tools import BaseTool, render_text_description_and_args
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


class ToolCallRequest(TypedDict):
    name: str
    arguments: Dict[str, Any]


def invoke_tool(
        tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None,
) -> str:
    """
    我们可以使用的执行工具调用的函数。

    :param tool_call_request: 一个包含键名和参数的字典，名称必须与现有的工具名称匹配，参数是该工具的参数。
    :param config: 这是LangChain中包含回调、元数据等信息的配置信息。
    :return: 工具执行的结果。
    """
    name = tool_call_request["name"]
    requested_tool = tools_dict.get(name)
    return requested_tool.invoke(tool_call_request.get("arguments"), config=config)


system_prompt = """
你是一个聊天机器人，可以访问以下工具
以下是每个工具的名称和描述

{rendered_tools}

根据用户输入，返回要使用的工具的名称和输入。
将您的响应作为具有`name`和`arguments`键的JSON块返回。
`arguments`应该是一个字典，其中键对应于参数名称，值对应于请求的值。
"""
prompt = ChatPromptTemplate.from_messages([
    ('system', system_prompt),
    ('human', "{query}")
]).partial(rendered_tools=render_text_description_and_args(tools))

llm = ChatOpenAI(model='deepseek-chat', temperature=0)
chain = prompt | llm | JsonOutputParser() | RunnablePassthrough.assign(output=invoke_tool)
print(chain.invoke('余姚今天天气怎么样'))
