# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: app运行时文件
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from fastapi.staticfiles import StaticFiles
from core.Router import AllRouter
from core.Events import startup, stopping
from core.Exception import http_error_handler, http422_error_handler, unicorn_exception_handler, UnicornException, \
    mysql_operational_error, mysql_does_not_exist
from core.Middleware import Middleware
from tortoise.exceptions import OperationalError, DoesNotExist

application = FastAPI(
    debug=settings.APP_DEBUG,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    title=settings.PROJECT_NAME
    )

# 事件监听
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))


# 异常错误处理
application.add_exception_handler(HTTPException, http_error_handler)
application.add_exception_handler(RequestValidationError, http422_error_handler)
application.add_exception_handler(UnicornException, unicorn_exception_handler)
application.add_exception_handler(DoesNotExist, mysql_does_not_exist)
application.add_exception_handler(OperationalError, mysql_operational_error)

# 路由
application.include_router(AllRouter)

# 中间件
application.add_middleware(Middleware)
application.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE,
    max_age=settings.SESSION_MAX_AGE
)
application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 静态资源目录
# application.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name="static")
# application.state.views = Jinja2Templates(directory=settings.TEMPLATE_DIR)

app = application

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)
