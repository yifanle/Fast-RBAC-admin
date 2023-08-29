# -*- coding:utf-8 -*-
"""
@Time : 2023/8/17 9:25
@Author: 李逸凡
@Des: 
"""
import math
from datetime import datetime

from tortoise.transactions import atomic

from core.Response import MiddleResponse, ResponseCode
from models.base import Role, Auth
from outdto.page import Page
from outdto.role import RoleDto
from schemas.page import PageParam
from schemas.role import UpdateRoleAuth, AddRole, UpdateRole


class RoleService:

    @atomic()
    async def page_list(self, page: PageParam) -> MiddleResponse:
        total_count = await Role.all().count()
        page_count = math.ceil(total_count / page.pageSize)
        pages = await Role.all().offset((page.page - 1) * page.pageSize).limit(page.pageSize)
        result_list = []
        for p in pages:
            role = RoleDto()
            role.id = p.pk
            role.role_name = p.role_name
            role.role_status = p.role_status
            role.role_desc = p.role_desc
            role.create_time = datetime.strftime(p.create_time, '%Y-%m-%d %H:%M:%S')
            role.update_time = datetime.strftime(p.update_time, '%Y-%m-%d %H:%M:%S')
            auth_list = await p.auth
            role.auth_keys = []
            for auth in auth_list:
                role.auth_keys.append(auth.permission)
            result_list.append(role)
        result = Page(list=result_list, pageCount=page_count, page=page.page, pageSize=page.pageSize)
        if len(result_list) > 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE, data=result)
        else:
            return MiddleResponse(ResponseCode.ROLE_QUERY_NOT_FOUND)

    @atomic()
    async def update_role_auth(self, param: UpdateRoleAuth) -> MiddleResponse:
        role = await Role().get_or_none(pk=param.role_id)
        if role is None:
            return MiddleResponse(ResponseCode.ROLE_NOT_FOUND)
        await role.auth.clear()
        auth_list = await Auth().filter(pk__in=param.auth_ids)
        for auth in auth_list:
            await role.auth.add(auth)
        return MiddleResponse(ResponseCode.SUCCESS_CODE)

    @atomic()
    async def add_role(self, param: AddRole) -> MiddleResponse:
        now_time = datetime.now()
        find_role = await Role().get_or_none(role_name=param.role_name)
        if find_role:
            return MiddleResponse(ResponseCode.ROLE_EXIST_ERROR)
        role = await Role().create(create_time=now_time, update_time=now_time, role_name=param.role_name,
                                   role_status=param.role_status, role_desc=param.role_desc)
        if role:
            return MiddleResponse(ResponseCode.SUCCESS_CODE, data=role)
        else:
            return MiddleResponse(ResponseCode.ROLE_CREATE_FAIL)

    @atomic()
    async def update_role(self, param: UpdateRole) -> MiddleResponse:
        now_time = datetime.now()
        exist_role = await Role.get_or_none(pk=param.id)
        if exist_role:
            if exist_role.role_name == '超级管理员' or exist_role.role_name == '普通用户':
                if param.role_name != '超级管理员' and param.role_name != '普通用户':
                    return MiddleResponse(ResponseCode.CHANGE_DEFAULT_ROLE_NAME_ERROR)
        else:
            return MiddleResponse(ResponseCode.ROLE_NOT_FOUND)
        row = await Role().filter(pk=param.id).update(update_time=now_time, role_name=param.role_name,
                                                      role_status=param.role_status, role_desc=param.role_desc)
        if row > 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)
        else:
            return MiddleResponse(ResponseCode.ROLE_UPDATE_FAIL)

    @atomic()
    async def del_role(self, param: UpdateRole) -> MiddleResponse:
        exist_role = await Role.get_or_none(pk=param.id)
        if exist_role:
            if exist_role.role_name == '超级管理员' or exist_role.role_name == '普通用户':
                return MiddleResponse(ResponseCode.DELETE_DEFAULT_ROLE_ERROR)
        row = await Role().filter(pk=param.id).delete()
        if row > 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)
        else:
            return MiddleResponse(ResponseCode.ROLE_DELETE_FAIL)

    @atomic()
    async def get_roles_options(self) -> MiddleResponse:
        roles = await Role().all()
        result_list = []
        if roles is None or len(roles) < 0:
            return MiddleResponse(ResponseCode.ROLE_QUERY_NOT_FOUND)
        for role in roles:
            option = {
                "label": role.role_name,
                "value": role.pk,
                "disabled": not role.role_status
            }
            result_list.append(option)
        return MiddleResponse(ResponseCode.SUCCESS_CODE, data=result_list)
