# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 3:40 PM
@Author: binkuolo
@Des: JWT鉴权
"""
from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import SecurityScopes
from fastapi.security.oauth2 import get_authorization_scheme_param, OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status
from config import settings
from models.base import User, Auth, Role
from typing import Optional

OAuth2 = OAuth2PasswordBearer("")


def create_access_token(user_id, user_type):
    """
    创建token
    """
    token_data = {
        "user_id": user_id,
        "user_type": user_type
    }
    # token超时时间
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 向jwt加入超时时间
    token_data.update({"exp": expire})
    # jwt加密
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token


async def check_permissions(req: Request, security_scopes: SecurityScopes, token=Depends(OAuth2)):
    """
    权限验证
    :param token:
    :param req:
    :param security_scopes: 权限域
    :return:
    """
    # ----------------------------------------验证JWT token------------------------------------------------------------
    print("token", token)
    print("scopes", security_scopes.scopes)
    # 从请求头获取token
    # authorization: str = req.headers.get("Authorization")
    # scheme, param = get_authorization_scheme_param(authorization)
    #
    # if not authorization or scheme.lower() != "bearer":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not authenticated",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #
    # # 取出 token
    # token = param
    try:
        # token解密
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload:
            # 用户ID
            user_id = payload.get("user_id", None)
            # 用户类型
            user_type = payload.get("user_type", None)
            # 无效用户信息
            if user_id is None or user_type is None:
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效凭证",
                    headers={"WWW-Authenticate": f"Bearer{token}"},
                )
                raise credentials_exception

        else:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
            raise credentials_exception

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已证过期",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    except (PyJWTError, ValidationError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    # ---------------------------------------验证权限-------------------------------------------------------------------
    # 查询用户是否真实有效、或者已经被禁用
    check_user = await User.get_or_none(id=user_id)
    if not check_user or check_user.user_status != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已经被管理员禁用!",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    # 判断是否设置了权限域
    if security_scopes.scopes:
        # 返回当前权限域
        print("当前域：", security_scopes.scopes)
        # 非超级管理员且当前域需要验证
        if not user_type and security_scopes.scopes:
            is_pass = await Auth.filter(role__user__id=user_id, is_check=True,
                                        permission__in=set(security_scopes.scopes),
                                        role__role_status=True)
            print("is_pass", is_pass)
            # 未查询到对应权限
            if not is_pass:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not permissions",
                    headers={"scopes": security_scopes.scope_str},
                )
    # 查询用户所有权限
    permissions: Optional[list] = await Auth.filter(role__user__id=user_id, is_check=True,
                                                    role__role_status=True).values_list("auth_name", "permission")
    print('user_scopes', permissions)
    # 缓存用户全部权限
    req.state.permissions = permissions
    req.state.token = token
    # 缓存用户ID
    req.state.user_id = user_id
    # 缓存用户类型
    req.state.user_type = user_type
