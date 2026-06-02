# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/1 20:58
# @FileName: langchain-tools使用.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.utils.function_calling import convert_to_openai_tool

search = DuckDuckGoSearchRun()

print(search.invoke('langchain最新版本是多少'))
print(convert_to_openai_tool(search))
