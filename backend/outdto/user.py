# -*- coding:utf-8 -*-
"""
@Time : 2023/8/22 15:50
@Author: 李逸凡
@Des: 
"""
from typing import Optional

from pydantic import BaseModel


class UserDto:
    id: int
    username: str
    user_type: bool
    password: str
    nickname: str
    user_phone: str
    user_email: str
    full_name: str
    user_status: int
    avatar: str
    sex: int
    desc: str
    client_host: str
    create_time: str
    update_time: str
    roles: list


class UserInfoOutDto(BaseModel):
    userId: int
    username: Optional[str]
    realName: Optional[str]
    password: Optional[str]
    type: Optional[bool]
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    token: Optional[str]
    status: int
    avatar: Optional[str]
    desc: Optional[str]
    sex: Optional[int]
    permissions: Optional[list]
