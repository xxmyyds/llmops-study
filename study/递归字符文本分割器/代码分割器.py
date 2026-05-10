# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/10 16:06
# @FileName: 代码分割器.py
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

loader = UnstructuredFileLoader('demo.py')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    # 每个chunk最大数量
    chunk_size=500,
    # 每个chunk允许重叠的数量
    chunk_overlap=50,
    # 添加索引
    add_start_index=True
)

chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(len(chunk.page_content))
