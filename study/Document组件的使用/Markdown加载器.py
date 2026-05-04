# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/4 13:44
# @FileName: Markdown加载器.py
from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader('项目API资料.md')
documents = loader.load()
print(documents)
print(len(documents))
print(documents[0].metadata)
