# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/15 22:10
# @FileName: 字符串拼接.py
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template('请讲一个关于{subject}的笑话') + ',让我开心一下,' + '请使用{language}语言'
print(prompt.invoke({
    'subject': '程序员',
    'language': 'python',
}).to_string())
