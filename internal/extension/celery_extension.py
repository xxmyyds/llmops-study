# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/15 20:17
# @FileName: celery_extension.py
from celery import Task, Celery
from flask import Flask


def init_app(app: Flask):
    """celery配置"""

    class FlaskTask(Task):
        """定义FlaskTask，确保celery在flask上下文中运行，这样可以访问flask配置，数据库等内容"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()

    app.extensions['celery'] = celery_app
