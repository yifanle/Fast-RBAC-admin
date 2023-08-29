# -*- coding:utf-8 -*-
"""
@Time : 2023/8/17 8:53
@Author: 李逸凡
@Des: 
"""
from pydantic import BaseModel


class PageParam(BaseModel):
    page: int
    pageSize: int
