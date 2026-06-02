# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/2 20:54
# @FileName: google_serper_tool.py

import dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description='执行谷歌搜索的查询语句')


google_serper = GoogleSerperRun(
    name='GoogleSerper',
    description='Google Search',
    api_wrapper=GoogleSerperAPIWrapper(),
)
print(google_serper.invoke('vue 的作者是谁'))
