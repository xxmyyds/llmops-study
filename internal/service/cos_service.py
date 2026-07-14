# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/13 19:54
# @FileName: cos_service.py
import hashlib
import os
import uuid
from dataclasses import dataclass
from datetime import datetime

from injector import inject
from qcloud_cos import CosS3Client, CosConfig
from werkzeug.datastructures import FileStorage

from internal.entity.upload_file_entity import ALLOWED_DOCUMENT_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS
from internal.exception import FailException
from internal.model import UploadFile
from internal.service.upload_file_service import UploadFileService


@inject
@dataclass
class CosService:
    """腾讯云对象存储服务"""
    upload_file_service: UploadFileService

    def uploadFile(self, file: FileStorage, only_image: bool = False) -> UploadFile:
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        file_name = file.filename
        extension = file_name.rsplit(".", 1)[-1] if "." in file_name else ""
        if extension.lower() not in (ALLOWED_DOCUMENT_EXTENSIONS + ALLOWED_IMAGE_EXTENSIONS):
            raise FailException(f"该.{extension}扩展的文件不允许上传")
        elif only_image and extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise FailException(f"该.{extension}扩展的文件不允许上传,请上传正确的图片")

        client = self._get_client()
        bucket = self._get_bucket()

        random_filename = str(uuid.uuid4()) + '.' + extension
        now = datetime.now()
        upload_filename = f"{now.year}/{now.month:02d}/{now.day:02d}/{random_filename}"

        file_content = file.stream.read()

        try:
            client.put_object(Bucket=bucket, Key=upload_filename, Body=file_content)
        except Exception as e:
            raise FailException('上传文件失败，请稍后重试')

        return self.upload_file_service.create_upload_file(
            account_id=account_id,
            name=file_name,
            key=upload_filename,
            size=len(file_content),
            extension=extension,
            mime_type=file.mimetype,
            hash=hashlib.sha3_256(file_content).hexdigest()
        )

    def downloadFile(self, key: str, target_file_path: str):
        """下载cos云端的文件到本地的指定路径"""
        client = self._get_client()
        bucket = self._get_bucket()
        client.download_file(bucket, key, target_file_path)

    @classmethod
    def get_file_url(cls, key: str) -> str:
        """根据传递的cos云端key获取图片实际的url地址"""
        cos_domain = os.getenv("COS_DOMAIN")
        if not cos_domain:
            bucket = os.getenv("COS_BUCKET")
            scheme = os.getenv("COS_SCHEME")
            region = os.getenv("COS_REGION")
            cos_domain = f"{scheme}://{bucket}.cos.{region}.myqcloud.com"

        return f"{cos_domain}/{key}"

    @classmethod
    def _get_client(cls) -> CosS3Client:
        conf = CosConfig(
            Region=os.getenv("COS_REGION"),
            SecretId=os.getenv("COS_SECRET_ID"),
            SecretKey=os.getenv("COS_SECRET_KEY"),
            Token=None,
            Scheme=os.getenv("COS_SCHEME", "http"),
        )

        return CosS3Client(conf)

    @classmethod
    def _get_bucket(cls) -> str:
        return os.getenv("COS_BUCKET")
