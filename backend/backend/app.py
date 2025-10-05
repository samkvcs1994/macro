"""FastAPI application bootstrap."""
from fastapi import FastAPI

from .routers import config, health, indices, series, vintages

app = FastAPI(title="Global Liquidity Indices API", version="0.1.0")

app.include_router(health.router)
app.include_router(config.router, prefix="/api/v1")
app.include_router(series.router, prefix="/api/v1")
app.include_router(indices.router, prefix="/api/v1")
app.include_router(vintages.router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Global Liquidity Indices API"}
