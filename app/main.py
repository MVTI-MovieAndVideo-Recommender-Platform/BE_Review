from contextlib import asynccontextmanager

from auth.jwt import verify_access_token
from database import mysql_conn
from fastapi import FastAPI, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from sqlalchemy.ext.asyncio import close_all_sessions
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mysql_conn.init_db()
    yield
    await close_all_sessions()


class DataValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        jwt = request.headers.get("jwt", None)
        print(jwt)
        if jwt:
            # 기타 검증 로직을 여기에 추가할 수 있습니다.
            # 검증이 통과하면 다음 미들웨어 또는 요청 핸들러로 넘어갑니다.
            request.state.token = (
                decode_jwt
                if (decode_jwt := (await verify_access_token(jwt)).get("token"))
                else None
            )
            print("request.state.token -> ", request.state.token)
        # # print(request.query_params.getlist("media_id[]"))
        response = await call_next(request)
        return response


app = FastAPI(lifespan=lifespan, root_path="/review")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)

app.add_middleware(DataValidationMiddleware)
app.include_router(router, prefix="")


# 예외 처리
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


# 예외 처리
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Login API_SERVER with FastAPI"}


@app.get("/healthcheck")
async def get_healthcheck():
    return {"status": "OK"}
