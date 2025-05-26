from fastapi import FastAPI
from app.api.dsdcheck_router import router as dsdcheck_router

app = FastAPI(title="DSD Check Service", version="1.0.0")

app.include_router(dsdcheck_router, prefix="/api/dsdcheck") 