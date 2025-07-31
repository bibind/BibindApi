"""Wrapper around the MinIO SDK used for file storage."""

from __future__ import annotations

from datetime import timedelta
from typing import List, Optional
from urllib.parse import urlparse

from app.config import minio_config
from app.utils.logger import logger

try:
    from minio import Minio
    from minio.error import S3Error
except Exception:  # pragma: no cover - library missing during tests
    Minio = None  # type: ignore
    S3Error = Exception  # type: ignore

_client: Minio | None = None

if Minio is not None and minio_config.MINIO_ENDPOINT:
    parsed = urlparse(minio_config.MINIO_ENDPOINT)
    _endpoint = parsed.netloc or parsed.path
    _client = Minio(
        _endpoint,
        access_key=minio_config.MINIO_ACCESS_KEY,
        secret_key=minio_config.MINIO_SECRET_KEY,
        secure=minio_config.MINIO_SECURE,
    )


def _ensure_bucket(bucket: str) -> None:
    if _client is None:
        raise RuntimeError("MinIO client is not configured")
    try:
        if not _client.bucket_exists(bucket):
            _client.make_bucket(bucket)
    except S3Error as exc:  # type: ignore[attr-defined]
        logger.error(f"Bucket check failed for {bucket}: {exc}")
        raise


def upload_file(bucket: str, file_path: str, object_name: str) -> bool:
    """Upload a file to the given bucket."""
    if _client is None:
        logger.error("MinIO client is not available")
        return False
    try:
        _ensure_bucket(bucket)
        _client.fput_object(bucket, object_name, file_path)
        return True
    except Exception as exc:  # pragma: no cover - network/IO
        logger.error(f"Failed to upload {object_name} to {bucket}: {exc}")
        return False


def download_file(bucket: str, object_name: str, destination: str) -> bool:
    """Download a file from a bucket."""
    if _client is None:
        logger.error("MinIO client is not available")
        return False
    try:
        _ensure_bucket(bucket)
        _client.fget_object(bucket, object_name, destination)
        return True
    except Exception as exc:  # pragma: no cover - network/IO
        logger.error(f"Failed to download {object_name} from {bucket}: {exc}")
        return False


def generate_presigned_url(bucket: str, object_name: str, expiry: int = 3600) -> str:
    """Generate a presigned URL for an object."""
    if _client is None:
        logger.error("MinIO client is not available")
        return ""
    try:
        _ensure_bucket(bucket)
        return _client.presigned_get_object(
            bucket, object_name, expires=timedelta(seconds=expiry)
        )
    except Exception as exc:  # pragma: no cover - network/IO
        logger.error(f"Failed to generate URL for {object_name} in {bucket}: {exc}")
        return ""


def list_files(bucket: str, prefix: Optional[str] = None) -> List[str]:
    """List files in a bucket."""
    if _client is None:
        logger.error("MinIO client is not available")
        return []
    try:
        _ensure_bucket(bucket)
        objects = _client.list_objects(bucket, prefix=prefix, recursive=True)
        return [obj.object_name for obj in objects]
    except Exception as exc:  # pragma: no cover - network/IO
        logger.error(f"Failed to list files in {bucket}: {exc}")
        return []


def delete_file(bucket: str, object_name: str) -> bool:
    """Delete an object from a bucket."""
    if _client is None:
        logger.error("MinIO client is not available")
        return False
    try:
        _client.remove_object(bucket, object_name)
        return True
    except Exception as exc:  # pragma: no cover - network/IO
        logger.error(f"Failed to delete {object_name} from {bucket}: {exc}")
        return False

__all__ = [
    "upload_file",
    "download_file",
    "generate_presigned_url",
    "list_files",
    "delete_file",
]
