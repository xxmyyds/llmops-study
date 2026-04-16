# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/12 18:58
# @FileName: conftest.py
import pytest

from app.http.app import app


@pytest.fixture
def client():
    """获取Flask应用的测试应用，并返回"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
