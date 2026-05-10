# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/10 18:38
# @FileName: 语义文档分割器.py
import dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

dotenv.load_dotenv()
loader = UnstructuredFileLoader('科幻短篇.txt')
documents = loader.load()

text_splitter = SemanticChunker(
    embeddings=DashScopeEmbeddings(model='text-embedding-v4'),
    number_of_chunks=10,
    sentence_split_regex="(?<=[。？！.?!])"
)
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(len(chunk.page_content))
