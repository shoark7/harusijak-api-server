from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# class StaticStorage(S3Boto3Storage):
    # location = settings.AWS_STATIC_LOCATION


class PoetMediaStorage(S3Boto3Storage):
    location = settings.AWS_POET_MEDIA_LOCATION


class PoemMediaStorage(S3Boto3Storage):
    location = settings.AWS_POEM_EDIA_LOCATION