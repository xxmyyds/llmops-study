# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/6 22:07
# @FileName: FileSystem使用.py
from langchain_community.document_loaders import FileSystemBlobLoader

loader = FileSystemBlobLoader('.', show_progress=True)

for blob in loader.yield_blobs():
    print(blob.as_string())
