# -*- coding:utf-8 -*-
"""
@Time : 2023/8/8 23:08
@Author: 李逸凡
@Des: 
"""
from datetime import datetime

from tortoise.expressions import Q
from tortoise.transactions import atomic

from core.Response import MiddleResponse, ResponseCode
from models.base import Auth
from outdto.auth import AuthInfo
from schemas.auth import UpdateAuth, CreateAuth


class AuthService:

    @atomic()
    async def del_auth(self, auth_id: int) -> MiddleResponse:
        child_list = await Auth.filter(pid=auth_id)
        if len(child_list) > 0:
            return MiddleResponse(ResponseCode.AUTH_TREE_CHILD_EXIST)
        is_exist = await Auth.get_or_none(pk=auth_id)
        if is_exist is None:
            return MiddleResponse(ResponseCode.AUTH_NOT_FOUND)
        row = await Auth.filter(pk=auth_id).delete()
        if row > 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)
        else:
            return MiddleResponse(ResponseCode.AUTH_DELETE_FAIL)

    @atomic()
    async def add_auth(self, auth: CreateAuth) -> MiddleResponse:
        find_one = await Auth.filter(Q(auth_name=auth.label) | Q(permission=auth.auth))
        if len(find_one) > 0:
            return MiddleResponse(ResponseCode.AUTH_EXIST_ERROR)
        else:
            created = await Auth.create(auth_name=auth.label, subtitle=auth.subtitle, pid=auth.pid,
                                        permission=auth.auth, auth_desc=auth.desc, is_check=auth.is_check,
                                        auth_type=auth.auth_type)
            if created:
                return MiddleResponse(ResponseCode.SUCCESS_CODE, data=created)
            else:
                return MiddleResponse(ResponseCode.AUTH_CREATE_FAIL)

    @atomic()
    async def update_auth(self, auth: UpdateAuth) -> MiddleResponse:
        result = await Auth.filter(pk=auth.id).update(auth_name=auth.label, subtitle=auth.subtitle,
                                                      is_check=auth.is_check, permission=auth.auth, auth_desc=auth.desc,
                                                      update_time=datetime.now())
        if result > 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)
        else:
            return MiddleResponse(ResponseCode.AUTH_UPDATE_FAIL)

    @atomic()
    async def get_auth_list(self) -> MiddleResponse:
        auth_list = await Auth.all()
        if len(auth_list) <= 0:
            return MiddleResponse(ResponseCode.AUTH_QUERY_NOT_FOUND)
        tree_data = self.list_to_tree(auth_list)
        return MiddleResponse(ResponseCode.SUCCESS_CODE, data=tree_data)

    def list_to_tree(self, auth_list: list[Auth]):
        level_one = {}
        level_two: list[AuthInfo] = []
        for auth in auth_list:
            node = AuthInfo(auth)
            if node.pid == 0:
                level_one.update({node.id: node})
            else:
                level_two.append(node)
        for two in level_two:
            level_one[two.pid].children.append(two)
        values = level_one.values()
        return list(values)
