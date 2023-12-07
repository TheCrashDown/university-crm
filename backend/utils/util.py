"""Some useful util functions"""

import os

import boto3

import logging

logger = logging.getLogger(__name__)


class Util:
    """Util class"""

    @staticmethod
    def s3_connect():
        client = boto3.Session().client(
            "s3",
            endpoint_url=os.environ.get("S3_ENDPOINT"),
            aws_access_key_id=os.environ.get("MINIO_ROOT_USER"),
            aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD"),
        )
        bucket = os.environ.get("S3_BUCKET")

        return client, bucket

    @classmethod
    def s3_read(cls, path):
        client, bucket = cls.s3_connect()
        response = client.get_object(Bucket=bucket, Key=path)
        content = response["Body"].read().decode("utf-8")
        return content

    @classmethod
    def s3_create(cls, path, content):
        client, bucket = cls.s3_connect()
        client.put_object(Bucket=bucket, Key=path, Body=content)

    @classmethod
    def s3_delete(cls, path):
        client, bucket = cls.s3_connect()
        client.delete_object(Bucket=bucket, Key=path)
