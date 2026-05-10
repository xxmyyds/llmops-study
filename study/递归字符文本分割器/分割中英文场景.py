# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/10 16:15
# @FileName: 分割中英文场景.py
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = UnstructuredMarkdownLoader('项目API资料.md')
documents = loader.load()
separators = [
    "\n\n",
    "\n",
    "。|！|？",
    "\.\s|\!\s|\?\s",
    "；|;\s",
    "，|,\s",
    " ",
    ""
]

text_splitter = RecursiveCharacterTextSplitter(
    separators=separators,
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
