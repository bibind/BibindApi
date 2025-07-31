"""Routes for simple file operations with MinIO."""

from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.clients import minio_client

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/{bucket}")
async def list_bucket_files(bucket: str, prefix: Optional[str] = None) -> JSONResponse:
    files = await asyncio.to_thread(minio_client.list_files, bucket, prefix)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"files": files})
