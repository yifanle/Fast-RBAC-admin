# -*- coding:utf-8 -*-
"""
@Time : 2023/8/17 7:59
@Author: 李逸凡
@Des: 
"""
from pydantic import BaseModel


class Page(BaseModel):
    page: int  # currentPage
    pageCount: int  # 总页数
    pageSize: int  # 一页数量
    list: list

