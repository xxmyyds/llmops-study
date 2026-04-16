# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/15 22:23
# @FileName: 复用提示模板.py
from langchain_core.prompts import PromptTemplate, PipelinePromptTemplate

full_template = PromptTemplate.from_template('{a}{b}{c}')

instruction_template = PromptTemplate.from_template('你正在模拟{person}')
example_template = PromptTemplate.from_template('下面是一个交互例子:'
                                                'Q:{example_q}'
                                                'A:{example_a}')
start_template = PromptTemplate.from_template('现在你是一个真实的人,请回答用户的问题：'
                                              'Q:{start_q}'
                                              'A:')

pipeline_prompt = PipelinePromptTemplate
