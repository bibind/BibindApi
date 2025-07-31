"""Human validation routes."""

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.services import validation_service

router = APIRouter(prefix="/validation", tags=["validation"])


@router.post("/approve/{event_id}")
async def approve(event_id: int) -> JSONResponse:
    ok = await validation_service.approve(event_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Event not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "approved"})


@router.post("/reject/{event_id}")
async def reject(event_id: int) -> JSONResponse:
    ok = await validation_service.reject(event_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Event not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "rejected"})


@router.get("/pending")
async def pending() -> JSONResponse:
    data = await validation_service.pending()
    return JSONResponse(status_code=200, content={"events": data})
