from fastapi import FastAPI
from app.api.xbrlgen_router import router as xbrl_router

app = FastAPI()
app.include_router(xbrl_router, prefix="/xbrlgen")
