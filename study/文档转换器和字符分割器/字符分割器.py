# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/8 21:44
# @FileName: 字符分割器.py
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter

loader = UnstructuredMarkdownLoader('项目API资料.md')
documents = loader.load()
print(documents)
print(len(documents))

text_splitter = CharacterTextSplitter(
    separator='\n\n',
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(len(chunk.page_content))
