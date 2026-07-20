# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/20 20:32
# @FileName: jieba_service.py
from dataclasses import dataclass

from injector import inject
from jieba.analyse import default_tfidf, extract_tags

from internal.entity.jieba_entity import STOPWORD_SET


@inject
@dataclass
class JiebaService:
    """结巴分词服务"""

    def __init__(self):
        default_tfidf.stop_words = STOPWORD_SET

    @classmethod
    def extract_keywords(cls, text: str, max_keyword_pre_chunk: int = 10) -> list[str]:
        """根据输入的文本，提取对应文本的关键词列表"""
        return extract_tags(sentence=text, topK=max_keyword_pre_chunk)
