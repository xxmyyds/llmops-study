# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/10 15:52
# @FileName: 递归字符文本分割器使用示例.py
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = UnstructuredMarkdownLoader('../../study/递归字符文本分割器/项目API资料.md')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
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
