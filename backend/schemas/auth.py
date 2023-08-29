# -*- coding:utf-8 -*-
"""
@Time : 2023/8/15 15:41
@Author: 李逸凡
@Des: 
"""
from pydantic import Field, BaseModel, validator
from typing import Optional

from schemas.validator import strip_validator


class UpdateAuth(BaseModel):
    id: int
    label: str
    subtitle: Optional[str]
    is_check: bool
    auth: str
    desc: Optional[str]

    @validator('*', pre=True)
    def pre_validate(cls, v):
        return strip_validator(v)


class CreateAuth(UpdateAuth):
    pid: int
    auth_type: int

