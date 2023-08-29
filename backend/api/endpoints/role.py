# -*- coding:utf-8 -*-
"""
@Time : 2023/8/17 7:55
@Author: 李逸凡
@Des: 
"""

from fastapi import APIRouter, Security, Depends

from core.Auth import check_permissions
from core.Response import response_code_handler
from schemas.page import PageParam
from schemas.role import UpdateRoleAuth, AddRole, UpdateRole
from service.RoleService import RoleService

router = APIRouter(prefix="/role")


@router.post("/page", summary="角色分页查询", dependencies=[Security(check_permissions, scopes=["role_list"])])
async def page_list(page: PageParam, service: RoleService = Depends(RoleService)):
    m = await service.page_list(page)
    return response_code_handler(m)


@router.post("/update_auth", summary="角色权限分配", dependencies=[Security(check_permissions, scopes=["role_update_auth"])])
async def update_role_auth(param: UpdateRoleAuth, service: RoleService = Depends(RoleService)):
    m = await service.update_role_auth(param)
    return response_code_handler(m)


@router.post("/add_role", summary="新建角色", dependencies=[Security(check_permissions, scopes=["role_add"])])
async def add_role(param: AddRole, service: RoleService = Depends(RoleService)):
    m = await service.add_role(param)
    return response_code_handler(m)


@router.post("/update_role", summary="更新角色", dependencies=[Security(check_permissions, scopes=["role_update"])])
async def update_role(param: UpdateRole, service: RoleService = Depends(RoleService)):
    m = await service.update_role(param)
    return response_code_handler(m)


@router.delete("/del_role", summary="删除角色", dependencies=[Security(check_permissions, scopes=["role_del"])])
async def del_role(param: UpdateRole, service: RoleService = Depends(RoleService)):
    m = await service.del_role(param)
    return response_code_handler(m)


@router.get("/get_roles_options", summary="获取所有角色options", dependencies=[Security(check_permissions, scopes=["roles_options"])])
async def get_roles_options(service: RoleService = Depends(RoleService)):
    m = await service.get_roles_options()
    return response_code_handler(m)

