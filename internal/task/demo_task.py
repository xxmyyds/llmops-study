# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/15 21:03
# @FileName: demo_task.py
import logging
import time
from uuid import UUID

from celery import shared_task
from flask import current_app


@shared_task
def demo_task(id: UUID) -> str:
    logging.info('睡眠5s')
    time.sleep(5)
    logging.info(f'id:{id}')
    logging.info(f'配置信息:{current_app.config}')
    return 'xxm'
