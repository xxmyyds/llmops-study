# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/6 21:42
# @FileName: Blob解析示例.py
from typing import Iterator

from langchain_core.document_loaders import BaseBlobParser
from langchain_core.documents import Document
from langchain_core.documents.base import Blob


class CustomParser(BaseBlobParser):
    """自定义文本解析器"""

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        line_number = 0
        with blob.as_bytes_io() as f:
            for line in f:
                yield Document(
                    page_content=line,
                    metadata={'source': blob.source, 'line_number': line_number},
                )
                line_number += 1


blob = Blob.from_path('./xx.txt')
parser = CustomParser()

documents = list(parser.lazy_parse(blob))
print(documents)
print(len(documents))
