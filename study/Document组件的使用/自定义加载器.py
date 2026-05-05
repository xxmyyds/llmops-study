# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/5 22:21
# @FileName: 自定义加载器.py
from typing import Iterator, AsyncIterator

import aiofiles
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class CustomDocumentLoader(BaseLoader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader for `Document`.

        Yields:
            The `Document` objects.
        """
        with open(self.file_path, encoding="utf-8") as f:
            line_number = 0
            for line in f:
                yield Document(
                    page_content=line,
                    metadata={"score": self.file_path, "line_number": line_number}
                )
                line_number += 1

    async def alazy_load(self) -> AsyncIterator[Document]:
        """An async lazy loader for `Document`.

                Yields:
                    The `Document` objects.
                """
        async with aiofiles.open(self.file_path, encoding="utf-8") as f:
            line_number = 0
            async for line in f:
                yield Document(
                    page_content=line,
                    metadata={"score": self.file_path, "line_number": line_number}
                )
                line_number += 1


loder = CustomDocumentLoader('./电商产品数据.txt')
documents = loder.load()
print(documents)
print(len(documents))
print(documents[0].metadata)
