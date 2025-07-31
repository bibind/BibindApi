from fastapi import FastAPI

from app.routes import auth

app = FastAPI(title="Operational Bootstrap")

# Include sample router
app.include_router(auth.router)


@app.get("/health")
async def health() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}
