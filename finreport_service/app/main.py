from fastapi import FastAPI
from dotenv import load_dotenv
from .api.xbrl_parser_router import router as xbrl_parser_router
from .api.opendart_router import router as opendart_router

load_dotenv()
app = FastAPI()

# ✅ prefix 적용
app.include_router(xbrl_parser_router, prefix="/xbrl")
app.include_router(opendart_router, prefix="/opendart")


@app.get("/")
def read_root():
    return {"Hello": "World"}
