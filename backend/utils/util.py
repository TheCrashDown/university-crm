"""Some useful util functions"""

import os
import logging

import boto3
import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)


class Util:
    """Util class"""

    @staticmethod
    def get_session():
        engine = create_engine(os.environ.get("POSTGRES_SECRET"))
        Session = sessionmaker(bind=engine)
        session = Session()

        return session

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

    @staticmethod
    def get_redis_client():
        return redis.Redis(host="redis", port=6379, db=0)

    @staticmethod
    def renew_token(r, token):
        r.expire(token, 3600)
