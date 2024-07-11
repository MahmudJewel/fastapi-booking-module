# fastapi 
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from starlette.middleware.sessions import SessionMiddleware

from app.api.routers.api import router
from app.core.settings import config, SECRET_KEY

def init_routers(app_: FastAPI) -> None:
    # url path 
    app_.include_router(router)


origins = [
    "*"
]

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            SessionMiddleware,
            secret_key=SECRET_KEY
        ),
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


# def init_cache() -> None:
#     Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

# def init_listeners(app_: FastAPI) -> None:
#     @app_.exception_handler(CustomException)
#     async def custom_exception_handler(request: Request, exc: CustomException):
#         return JSONResponse(
#             status_code=exc.code,
#             content={"error_code": exc.error_code, "message": exc.message},
#         )
