# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 5:24 PM
@Author: 李逸凡
@Des: 用户管理
"""
from core.Response import response_code_handler
from outdto.user import UserInfoOutDto
from schemas.page import PageParam
from schemas.user import CreateUser, AccountLogin, UserRoles, UpdateUser, UpdatePwd
from core.Auth import check_permissions
from fastapi import Request, APIRouter, Security, Depends

from service.UserService import UserService

router = APIRouter(prefix="/user")


@router.get("/info", summary="获取当前用户信息", dependencies=[Security(check_permissions)])
async def user_info(req: Request, service: UserService = Depends(UserService)):
    """
    获取当前登陆用户信息
    :return:
    """
    m = await service.get_user_info(req)
    return response_code_handler(m)


@router.get("/reset_pwd", summary="重置密码", dependencies=[Security(check_permissions, scopes=["user_up_pwd"])])
async def reset_pwd(user_id: int, service: UserService = Depends(UserService)):
    m = await service.reset_pwd(user_id)
    return response_code_handler(m)


@router.post("/login", summary="用户登陆")
async def account_login(login_dto: AccountLogin, service: UserService = Depends(UserService)):
    m = await service.login(login_dto)
    return response_code_handler(m)
    # return JSONResponse(success(msg='登录成功'), status_code=200, headers={"Set-Cookie": "X-token=Bearer "+jwt_token})


@router.post("/page", summary="角色分页查询", dependencies=[Security(check_permissions, scopes=["user_list"])])
async def page_list(page: PageParam, service: UserService = Depends(UserService)):
    m = await service.page_list(page)
    return response_code_handler(m)


@router.post("/update_user_role", summary="用户角色更新", dependencies=[Security(check_permissions, scopes=["update_user_role"])])
async def update_roles(param: UserRoles, service: UserService = Depends(UserService)):
    m = await service.update_roles(param)
    return response_code_handler(m)


# @router.post("/add", summary="用户添加", dependencies=[Security(check_permissions, scopes=["user_add", "user_list"])])
@router.post("/add", summary="用户添加", dependencies=[Security(check_permissions, scopes=["user_add"])])
async def user_add(post: CreateUser, service: UserService = Depends(UserService)):
    m = await service.user_add(post)
    return response_code_handler(m)


@router.post("/update", summary="用户更新", dependencies=[Security(check_permissions, scopes=["user_update"])])
async def user_update(param: UpdateUser, service: UserService = Depends(UserService)):
    m = await service.user_update(param)
    return response_code_handler(m)


@router.delete("/del", summary="用户删除", dependencies=[Security(check_permissions, scopes=["user_del"])])
async def user_del(user_id: int, service: UserService = Depends(UserService)):
    m = await service.user_del(user_id)
    return response_code_handler(m)


@router.post("/profile/account", summary="更新基本信息", dependencies=[Security(check_permissions, scopes=["update_profile"])])
async def update_profile(param: UserInfoOutDto, service: UserService = Depends(UserService)):
    m = await service.update_profile(param)
    return response_code_handler(m)


@router.post("/profile/pwd_modify", summary="修改密码", dependencies=[Security(check_permissions, scopes=["update_profile"])])
async def modify_pwd(req: Request, param: UpdatePwd, service: UserService = Depends(UserService)):
    m = await service.modify_pwd(req.state.user_id, param)
    return response_code_handler(m)
