from fastapi import FastAPI
from dotenv import load_dotenv
from .api.xbrl_parser_router import router as xbrl_parser_router
from .api.opendart_router import router as opendart_router

load_dotenv()
app = FastAPI()

# 라우터에 이미 prefix가 설정되어 있으므로 추가 prefix 없이 등록
app.include_router(xbrl_parser_router)
app.include_router(opendart_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
