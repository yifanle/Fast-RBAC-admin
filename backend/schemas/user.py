# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 5:29 PM
@Author: 李逸凡
@Des: 用户验证模型
"""
from pydantic import Field, BaseModel, validator
from typing import Optional

from schemas.validator import strip_validator, full_name_validator, phone_validator, email_validator


class UpdateUser(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=20)
    nickname: Optional[str]
    user_type: bool
    user_status: int
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str] = Field(min_length=1, max_length=5)
    desc: Optional[str]
    sex: int

    @validator('*', pre=True)
    def pre_validate(cls, v):
        return strip_validator(v)

    @validator('full_name')
    def full_name_validate(cls, v):
        assert full_name_validator(v)
        return v

    @validator('user_phone')
    def phone_validator(cls, v):
        assert phone_validator(v)
        return v

    @validator('user_email')
    def email_validator(cls, v):
        assert email_validator(v)
        return v


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6)
    nickname: Optional[str]
    user_type: bool
    user_status: int
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str] = Field(min_length=1, max_length=5)
    desc: Optional[str]
    sex: int

    @validator('*', pre=True)
    def pre_validate(cls, v):
        return strip_validator(v)

    @validator('full_name')
    def full_name_validate(cls, v):
        assert full_name_validator(v)
        return v

    @validator('user_phone')
    def phone_validator(cls, v):
        assert phone_validator(v)
        return v

    @validator('user_email')
    def email_validator(cls, v):
        assert email_validator(v)
        return v


class UserRoles(BaseModel):
    id: int
    roles: list


class AccountLogin(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6)


class UpdatePwd(BaseModel):
    oldPassword: str
    newPassword: str


