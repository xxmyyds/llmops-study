# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/11 21:55
# @FileName: 自定义分割器.py
import jieba.analyse
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import TextSplitter

loader = UnstructuredFileLoader('科幻短篇.txt')
documents = loader.load()


class CustomTextSplitter(TextSplitter):
    """自定义文档分割器"""

    def __init__(self, separator: str, top_k: int = 10, **kwargs):
        """构造函数，传递分割器还有需要提取的关键词数，默认为10"""
        super().__init__(**kwargs)
        self._separator = separator
        self._top_k = top_k

    def split_text(self, text: str) -> list[str]:
        split_texts = text.split(self._separator)

        text_keywords = []
        # 提取分割出来的每一段文本的关键词，默认10个
        for split_text in split_texts:
            text_keywords.append(jieba.analyse.extract_tags(split_text, topK=self._top_k))

        return [",".join(keywords) for keywords in text_keywords]


text_splitter = CustomTextSplitter('\n\n', 10)

chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(chunk.page_content)
