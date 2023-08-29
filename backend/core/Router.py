# -*- coding:utf-8 -*-
"""
@Time : 2022/4/23 11:43 AM
@Author: 李逸凡
@Des: 路由聚合
"""
from api.Base import api_router
from fastapi import APIRouter


AllRouter = APIRouter()
# API路由
AllRouter.include_router(api_router)

