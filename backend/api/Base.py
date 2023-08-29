# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: 李逸凡
@Des: 基本路由
"""
from fastapi import APIRouter

from api.endpoints import user, auth, role

api_router = APIRouter(prefix="/api")

api_router.include_router(user.router, prefix='/admin', tags=["用户管理"])
api_router.include_router(auth.router, prefix='/admin', tags=["权限管理"])
api_router.include_router(role.router, prefix='/admin', tags=["角色管理"])
