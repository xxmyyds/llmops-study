# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/4 14:11
# @FileName: URL加载器.py
from langchain_community.document_loaders import WebBaseLoader

url_loader = WebBaseLoader('http://www.bilibili.com/')
url_documents = url_loader.load()
print(url_documents)
print(len(url_documents))
print(url_documents[0].metadata)
