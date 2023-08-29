# -*- coding:utf-8 -*-
"""
@Time : 2023/8/5 13:36
@Author: 李逸凡
@Des: 
"""
import math
from datetime import datetime

from tortoise.transactions import atomic

from core.Auth import create_access_token
from core.Response import ResponseCode, MiddleResponse
from core.Utils import check_password, sha256_hash
from models.base import User, Role
from outdto.page import Page
from outdto.user import UserDto, UserInfoOutDto
from schemas.page import PageParam
from schemas.user import AccountLogin, UserRoles, CreateUser, UpdateUser, UpdatePwd
from fastapi import Request


class UserService:

    @atomic()
    async def user_add(self, post: CreateUser) -> MiddleResponse:
        find_user = await User.get_or_none(username=post.username)
        if find_user:
            return MiddleResponse(ResponseCode.USER_EXIST_ERROR)
        create_user = await User.create(**post.dict())
        if not create_user:
            return MiddleResponse(ResponseCode.USER_CREATE_FAIL)
        if create_user.user_type:
            super_role = await Role.get_or_none(role_name='超级管理员')
            await create_user.role.add(super_role)
        else:
            normal_role = await Role.get_or_none(role_name='普通用户')
            await create_user.role.add(normal_role)
        return MiddleResponse(ResponseCode.SUCCESS_CODE)

    @atomic()
    async def update_roles(self, param: UserRoles) -> MiddleResponse:
        user = await User().get_or_none(pk=param.id)
        if user is None:
            return MiddleResponse(ResponseCode.USER_NOT_FOUND)
        await user.role.clear()
        role_list = await Role().filter(pk__in=param.roles)
        if len(role_list) <= 0:
            return MiddleResponse(ResponseCode.ROLE_NOT_FOUND)
        for role in role_list:
            await user.role.add(role)
        return MiddleResponse(ResponseCode.SUCCESS_CODE)

    @atomic()
    async def page_list(self, page: PageParam) -> MiddleResponse:
        total_count = await User.all().count()
        page_count = math.ceil(total_count / page.pageSize)
        pages = await User.all().offset((page.page - 1) * page.pageSize).limit(page.pageSize)
        result_list = []
        for p in pages:
            user = UserDto()
            user.id = p.pk
            user.username = p.username
            user.user_type = p.user_type
            user.nickname = p.nickname
            user.create_time = datetime.strftime(p.create_time, '%Y-%m-%d %H:%M:%S')
            user.update_time = datetime.strftime(p.update_time, '%Y-%m-%d %H:%M:%S')
            user.user_phone = p.user_phone
            user.user_email = p.user_email
            user.full_name = p.full_name
            user.user_status = p.user_status
            user.avatar = p.avatar
            user.sex = p.sex
            user.desc = p.desc
            user.client_host = p.client_host
            role_list = await p.role
            user.roles = []
            for role in role_list:
                user.roles.append(role.pk)
            result_list.append(user)
        result = Page(list=result_list, pageCount=page_count, page=page.page, pageSize=page.pageSize)
        if len(result_list) > 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE, data=result)
        else:
            return MiddleResponse(ResponseCode.USER_QUERY_NOT_FOUND)

    @atomic()
    async def get_user_info(self, req: Request) -> MiddleResponse:
        user_data = await User.get_or_none(pk=req.state.user_id)
        if not user_data:
            # return fail(msg=f"用户不存在!")
            return MiddleResponse(ResponseCode.USER_NOT_FOUND)
        info = UserInfoOutDto(
            userId=user_data.pk,
            username=user_data.username,
            realName=user_data.full_name,
            avatar=user_data.avatar,
            desc=user_data.desc,
            user_phone=user_data.user_phone,
            user_email=user_data.user_email,
            token=req.state.token,
            type=user_data.user_type,  # True为管理员
            nickname=user_data.nickname,
            status=user_data.user_status,
            sex=user_data.sex
        )
        permission_list = []
        permissions = req.state.permissions
        for permission in permissions:
            p = {
                "label": permission[0],
                "value": permission[1],
            }
            permission_list.append(p)
        info.permissions = permission_list
        return MiddleResponse(ResponseCode.SUCCESS_CODE, data=info)

    @atomic()
    async def reset_pwd(self, user_id: int) -> MiddleResponse:
        user = await User.get_or_none(id=user_id)
        if user:
            encode_pwd = sha256_hash('123456')
            result_row = await User.filter(id=user_id).update(password=encode_pwd)
            if result_row < 0:
                return MiddleResponse(ResponseCode.PWD_MODIFY_FAIL)
        else:
            return MiddleResponse(ResponseCode.USER_NOT_FOUND)
        return MiddleResponse(ResponseCode.SUCCESS_CODE)

    @atomic()
    async def login(self, login_dto: AccountLogin) -> MiddleResponse:
        get_user = await User.get_or_none(username=login_dto.username)
        if not get_user or not check_password(login_dto.password, get_user.password):
            return MiddleResponse(ResponseCode.PWD_INCORRECT_ERROR)
        if not get_user.user_status:
            return MiddleResponse(ResponseCode.USER_BANED_ERROR)

        jwt_token = create_access_token(user_id=get_user.pk, user_type=get_user.user_type)
        return MiddleResponse(ResponseCode.SUCCESS_CODE, data={"token": jwt_token})

    @atomic()
    async def user_update(self, param: UpdateUser) -> MiddleResponse:
        rows = await User.filter(pk=param.id).update(username=param.username,
                                                     nickname=param.nickname,
                                                     user_type=param.user_type,
                                                     user_status=param.user_status,
                                                     user_phone=param.user_phone,
                                                     user_email=param.user_email,
                                                     full_name=param.full_name,
                                                     desc=param.desc,
                                                     sex=param.sex)
        if rows >= 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)
        else:
            return MiddleResponse(ResponseCode.USER_UPDATE_FAIL)

    @atomic()
    async def user_del(self, user_id) -> MiddleResponse:
        delete_user = await User.filter(pk=user_id).delete()
        if not delete_user:
            return MiddleResponse(ResponseCode.USER_DELETE_FAIL)
        return MiddleResponse(ResponseCode.SUCCESS_CODE)

    @atomic()
    async def update_profile(self, param: UserInfoOutDto) -> MiddleResponse:
        user = await User.get_or_none(pk=param.userId)
        if user is None:
            return MiddleResponse(ResponseCode.USER_NOT_FOUND)
        rows = await User.filter(pk=param.userId).update(nickname=param.nickname,
                                                         user_phone=param.user_phone,
                                                         user_email=param.user_email,
                                                         full_name=param.realName,
                                                         desc=param.desc,
                                                         sex=param.sex)
        if rows >= 0:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)
        else:
            return MiddleResponse(ResponseCode.USER_UPDATE_FAIL)

    @atomic()
    async def modify_pwd(self, user_id, param: UpdatePwd):
        user = await User.get_or_none(pk=user_id)
        if user is None:
            return MiddleResponse(ResponseCode.USER_NOT_FOUND)
        if param.oldPassword != user.password:
            return MiddleResponse(ResponseCode.USER_OLD_PASSWORD_INCORRECT)
        if param.newPassword == user.password:
            return MiddleResponse(ResponseCode.USER_PWD_OLD_NEW_SAME)
        result_row = await User.filter(id=user_id).update(password=param.newPassword)
        if result_row < 0:
            return MiddleResponse(ResponseCode.PWD_MODIFY_FAIL)
        else:
            return MiddleResponse(ResponseCode.SUCCESS_CODE)


