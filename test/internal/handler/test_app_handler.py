# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/12 11:24
# @FileName: test_app_handler.py
import pytest

from pkg.response import HttpCode


class TestAppHandler:
    @pytest.mark.parametrize("query", [None, "你是谁"])
    def test_completion(self, query, client):
        res = client.post("/app/completion", json={"query": query})
        assert res.status_code == 200
        if query is None:
            assert res.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert res.json.get("code") == HttpCode.SUCCESS
        print("响应内容", res.json)
