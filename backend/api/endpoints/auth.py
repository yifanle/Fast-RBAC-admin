# -*- coding:utf-8 -*-
"""
@Time : 2023/8/8 8:55
@Author: 李逸凡
@Des: 
"""

from fastapi import APIRouter, Security, Depends

from core.Auth import check_permissions
from core.Response import response_code_handler
from schemas.auth import UpdateAuth, CreateAuth
from service.AuthService import AuthService

router = APIRouter(prefix="/user_auth")


@router.get("/list", summary="权限查询", dependencies=[Security(check_permissions, scopes=["auth_list"])])
async def get_auth_list(service: AuthService = Depends(AuthService)):
    m = await service.get_auth_list()
    return response_code_handler(m)


@router.post("/add", summary="添加权限", dependencies=[Security(check_permissions, scopes=["auth_add"])])
async def add_auth(auth: CreateAuth, service: AuthService = Depends(AuthService)):
    m = await service.add_auth(auth)
    return response_code_handler(m)


@router.delete("/del", summary="删除权限", dependencies=[Security(check_permissions, scopes=["auth_del"])])
async def del_auth(auth_id: int, service: AuthService = Depends(AuthService)):
    m = await service.del_auth(auth_id)
    return response_code_handler(m)


@router.post("/update", summary="修改权限", dependencies=[Security(check_permissions, scopes=["auth_update"])])
async def update_auth(auth: UpdateAuth, service: AuthService = Depends(AuthService)):
    m = await service.update_auth(auth)
    return response_code_handler(m)

