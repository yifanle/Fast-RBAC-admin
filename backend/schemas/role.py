# -*- coding:utf-8 -*-
"""
@Time : 2023/8/18 20:47
@Author: 李逸凡
@Des: 
"""
from typing import Optional

from pydantic import BaseModel, validator

from schemas.validator import strip_validator


class UpdateRoleAuth(BaseModel):
    role_id: int
    auth_ids: list[int]


class AddRole(BaseModel):
    role_name: Optional[str]
    role_status: bool
    role_desc: Optional[str]

    @validator('*', pre=True)
    def pre_validate(cls, v):
        return strip_validator(v)


class UpdateRole(AddRole):
    id: int
