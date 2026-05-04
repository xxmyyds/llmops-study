# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/4 13:20
# @FileName: TextLoader的使用.py
from langchain_community.document_loaders import TextLoader

loader = TextLoader('./电商产品数据.txt', encoding='utf-8')

document = loader.load()

print(document)
print(len(document))
print(document[0].metadata)
