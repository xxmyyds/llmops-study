# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/19 18:33
# @FileName: embeddings_service.py
import os
from dataclasses import dataclass
from pathlib import Path

import tiktoken
from injector import inject
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.storage import RedisStore
from langchain_core.embeddings import Embeddings
from redis import Redis


@inject
@dataclass
class EmbeddingsService:
    """文本嵌入模型服务"""
    _store: RedisStore
    _embeddings: Embeddings
    _cache_backed_embeddings: CacheBackedEmbeddings

    def __init__(self, redis: Redis) -> None:
        project_root = Path(__file__).parent.parent.parent
        print(project_root)
        cache_folder = os.path.join(project_root, 'internal', 'core', 'embeddings')
        self._store = RedisStore(client=redis)
        self._embeddings = HuggingFaceEmbeddings(
            model_name='nomic-ai/nomic-embed-text-v1.5',
            cache_folder=cache_folder,
            model_kwargs={
                'trust_remote_code': True,
            }
        )
        # self._embeddings = DashScopeEmbeddings(
        #     model='text-embedding-v4',
        #     dashscope_api_key=os.environ['DASHSCOPE_API_KEY'],
        # )
        self._cache_backed_embeddings = CacheBackedEmbeddings.from_bytes_store(
            self._embeddings,
            self._store,
            namespace='embeddings',
        )

    @classmethod
    def calculate_token_counts(cls, query: str) -> int:
        """计算传入文本的token数"""
        encoding = tiktoken.encoding_for_model('gpt-3.5')
        return len(encoding.encode(query))

    @property
    def store(self) -> RedisStore:
        return self._store

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings

    @property
    def cache_backed_embeddings(self) -> CacheBackedEmbeddings:
        return self._cache_backed_embeddings
