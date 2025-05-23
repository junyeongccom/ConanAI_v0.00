from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.stocktrend_router import router

app = FastAPI(
    title="Stocktrend Service",
    description="Service for stock trend analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Stocktrend Service"}

print(f"🤍0 메인 진입")